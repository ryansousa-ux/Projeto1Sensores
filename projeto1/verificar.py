"""Verificador do Projeto 1 — rode com: python verificar.py

Cada teste confere um comportamento pedido nas docstrings. Não altere este arquivo:
o professor roda exatamente esta versão na correção.
"""

import os

from leitor_inmet import (
    ErroFormatoArquivo,
    agrupar_por_mes,
    extrair_coluna,
    ler_metadados,
    ler_registros,
)
from relatorio import contar_motivos, resumir, salvar_relatorio
from validadores import (
    ErroCampoAusente,
    ErroDeSensor,
    ErroLeituraInvalida,
    ErroTipoInvalido,
    converter_leitura,
    validar_faixa,
    validar_lote,
    validar_tipo,
)

TOTAL_TESTES = 25  # um grupo que quebra no meio não pode "encolher" a prova
CSV = "dados/INMET_NE_MA_A203_SAO LUIS_01-01-2025_A_31-12-2025.CSV"


def lanca(excecao, funcao, *args):
    """True se funcao(*args) lançar exatamente a exceção esperada (ou uma subclasse dela)."""
    try:
        funcao(*args)
    except excecao:
        return True
    except Exception:
        return False
    return False


def testes_validadores():
    yield "converter '27,5' -> 27.5", converter_leitura("27,5") == 27.5
    yield "converter ' 0 ' -> 0.0", converter_leitura(" 0 ") == 0.0
    yield (
        "converter '' lança ErroCampoAusente",
        lanca(ErroCampoAusente, converter_leitura, ""),
    )
    yield (
        "converter 'abc' lança ErroTipoInvalido",
        lanca(ErroTipoInvalido, converter_leitura, "abc"),
    )
    yield (
        "exceções herdam de ErroDeSensor",
        all(
            issubclass(e, ErroDeSensor)
            for e in (ErroCampoAusente, ErroTipoInvalido, ErroLeituraInvalida)
        ),
    )
    yield (
        "validar_tipo('5') lança ErroTipoInvalido",
        lanca(ErroTipoInvalido, validar_tipo, "5"),
    )
    yield (
        "validar_tipo(True) lança ErroTipoInvalido",
        lanca(ErroTipoInvalido, validar_tipo, True),
    )
    yield "validar_faixa(500) retorna 500", validar_faixa(500) == 500
    yield (
        "validar_faixa(-1) lança ErroLeituraInvalida",
        lanca(ErroLeituraInvalida, validar_faixa, -1),
    )
    yield (
        "validar_faixa nos limites é válido",
        validar_faixa(0) == 0 and validar_faixa(1000) == 1000,
    )
    validas, invalidas = validar_lote(["1,5", "", "x", 2000, 7], 0, 1000)
    yield "validar_lote: válidas", validas == [1.5, 7]
    yield (
        "validar_lote: inválidas",
        invalidas
        == [
            ("", "ErroCampoAusente"),
            ("x", "ErroTipoInvalido"),
            (2000, "ErroLeituraInvalida"),
        ],
    )


def testes_leitor():
    meta = ler_metadados(CSV)
    yield "metadados: estação", meta.get("ESTACAO") == "SAO LUIS"
    yield "metadados: código", meta.get("CODIGO (WMO)") == "A203"
    registros = ler_registros(CSV)
    yield "8760 registros horários", len(registros) == 8760
    temperaturas = extrair_coluna(registros, "temperatura")
    yield "primeira temperatura é '27,5'", temperaturas[0] == "27,5"
    yield (
        "apelido inexistente lança KeyError",
        lanca(KeyError, extrair_coluna, registros, "pressao"),
    )
    meses = agrupar_por_mes(registros, "chuva")
    yield (
        "12 meses agrupados, em ordem",
        list(meses) == [f"2025/{m:02d}" for m in range(1, 13)],
    )
    yield "fevereiro tem 672 horas", len(meses["2025/02"]) == 672
    yield (
        "arquivo errado lança ErroFormatoArquivo",
        lanca(ErroFormatoArquivo, ler_metadados, "main.py"),
    )
    yield (
        "arquivo inexistente lança FileNotFoundError",
        lanca(FileNotFoundError, ler_registros, "nao.csv"),
    )


def testes_relatorio():
    yield "resumir([]) retorna None", resumir([]) is None
    yield (
        "resumir([1, 2, 4])",
        resumir([1, 2, 4]) == {"minimo": 1, "maximo": 4, "media": 2.33, "soma": 7},
    )
    yield (
        "contar_motivos",
        contar_motivos([("", "A"), ("x", "B"), ("", "A")]) == {"A": 2, "B": 1},
    )
    salvar_relatorio("_teste.txt", "ação ✅")
    with open("_teste.txt", encoding="utf-8") as f:
        yield "salvar_relatorio grava em UTF-8", f.read() == "ação ✅"
    os.remove("_teste.txt")


def rodar(nome, gerador):
    """Roda um grupo de testes; um erro inesperado reprova o restante do grupo."""
    aprovados = total = 0
    print(f"\n[{nome}]")
    try:
        for descricao, ok in gerador():
            total += 1
            aprovados += bool(ok)
            print(f"  {'✅' if ok else '❌'} {descricao}")
    except Exception as e:
        total += 1
        print(f"  💥 parou com {type(e).__name__}: {e}")
    return aprovados, total


if __name__ == "__main__":
    soma_ok = 0
    for nome, grupo in (
        ("validadores", testes_validadores),
        ("leitor_inmet", testes_leitor),
        ("relatorio", testes_relatorio),
    ):
        ok, _ = rodar(nome, grupo)
        soma_ok += ok
    print(f"\nResultado: {soma_ok}/{TOTAL_TESTES} testes passaram")
