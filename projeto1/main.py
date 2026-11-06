"""Relatório anual de uma estação meteorológica do INMET — Projeto 1.

Este arquivo JÁ ESTÁ PRONTO: ele mostra como os seus módulos serão usados.
Não altere este arquivo — implemente validadores.py, leitor_inmet.py e relatorio.py.

Uso:
    python main.py                       # usa o arquivo padrão em dados/
    python main.py caminho/do/outro.CSV  # outra estação ou outro ano
"""

import sys

from leitor_inmet import (
    ErroFormatoArquivo,
    agrupar_por_mes,
    extrair_coluna,
    ler_metadados,
    ler_registros,
)
from relatorio import contar_motivos, formatar_linha_variavel, resumir, salvar_relatorio
from validadores import ErroDeSensor, validar_faixa, validar_lote

CAMINHO_PADRAO = "dados/INMET_NE_MA_A203_SAO LUIS_01-01-2025_A_31-12-2025.CSV"
CAMINHO_SAIDA = "relatorio.txt"

# apelido -> (unidade, mínimo plausível, máximo plausível)
FAIXAS = {
    "temperatura": ("°C", 10, 45),
    "umidade": ("%", 0, 100),
    "chuva": ("mm", 0, 100),
    "vento": ("m/s", 0, 40),
}


def demonstrar_validadores():
    """Parte 1: o módulo validadores com dados de exemplo."""
    leituras = [45.2, 78.0, -5, "erro", 1200, 300.5, "27,4", ""]
    print("Validando leituras uma a uma:")
    for leitura in leituras:
        try:
            validar_faixa(leitura)
            print(f"  ✅ {leitura!r} válida")
        except ErroDeSensor as e:
            print(f"  ❌ {leitura!r}: {type(e).__name__} — {e}")
    validas, invalidas = validar_lote(leituras)
    print(
        f"Em lote: {len(validas)} válidas {validas}, {len(invalidas)} inválidas {invalidas}\n"
    )


def montar_relatorio(caminho):
    """Parte 2: lê o CSV real e monta o texto do relatório."""
    metadados = ler_metadados(caminho)
    registros = ler_registros(caminho)

    linhas = [
        f"Estação {metadados['ESTACAO']} ({metadados['CODIGO (WMO)']}) — {metadados['UF']}",
        f"Registros horários lidos: {len(registros)}",
        "",
        "== Resumo anual ==",
    ]
    for apelido, (unidade, minimo, maximo) in FAIXAS.items():
        validas, invalidas = validar_lote(
            extrair_coluna(registros, apelido), minimo, maximo
        )
        linhas.append(formatar_linha_variavel(apelido, unidade, validas, invalidas))
        if invalidas:
            linhas.append(f"{'':<18} motivos: {contar_motivos(invalidas)}")

    linhas += [
        "",
        "== Mês a mês ==",
        "mês      temp. média (°C)  chuva total (mm)  vento médio (m/s)",
    ]
    temperatura = agrupar_por_mes(registros, "temperatura")
    chuva = agrupar_por_mes(registros, "chuva")
    vento = agrupar_por_mes(registros, "vento")
    for mes in temperatura:
        temp = resumir(validar_lote(temperatura[mes], 10, 45)[0])
        mm = resumir(validar_lote(chuva[mes], 0, 100)[0])
        ms = resumir(validar_lote(vento[mes], 0, 40)[0])
        linhas.append(
            f"{mes}  {temp['media'] if temp else '—':>16}  "
            f"{mm['soma'] if mm else '—':>16}  {ms['media'] if ms else 'SEM DADOS':>17}"
        )
    return "\n".join(linhas) + "\n"


if __name__ == "__main__":
    demonstrar_validadores()
    caminho = sys.argv[1] if len(sys.argv) > 1 else CAMINHO_PADRAO
    try:
        texto = montar_relatorio(caminho)
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {caminho}")
    except ErroFormatoArquivo as e:
        print(f"❌ O arquivo não parece um CSV do INMET: {e}")
    else:
        print(texto)
        salvar_relatorio(CAMINHO_SAIDA, texto)
        print(f"✅ Relatório salvo em {CAMINHO_SAIDA}")
    finally:
        print("Processamento encerrado.")
