"""Estatísticas e relatório em texto — Projeto 1, Técnicas de Programação."""


def resumir(valores):
    """Retorna {"minimo", "maximo", "media", "soma"} de uma lista de números.

    Lista vazia NÃO é erro de programa: é um sensor que não mediu nada no período.
    Nesse caso, retorna None.
    """
    pass  # ← implemente aqui


def contar_motivos(invalidas):
    """Conta quantas leituras inválidas há por motivo.

    Recebe a lista de tuplas (leitura, nome_da_excecao) devolvida por validar_lote.
    Ex.: {"ErroCampoAusente": 12, "ErroLeituraInvalida": 1}
    """
    pass  # ← implemente aqui


def formatar_linha_variavel(apelido, unidade, validas, invalidas):
    """Uma linha do resumo anual. Sensor sem dados aparece como "SEM DADOS"."""
    total = len(validas) + len(invalidas)
    estat = resumir(validas)
    if estat is None:
        return f"{apelido:<12} {unidade:<5} SEM DADOS ({total} falhas)"
    return (
        f"{apelido:<12} {unidade:<5} min {estat['minimo']:>7.1f}  "
        f"max {estat['maximo']:>7.1f}  media {estat['media']:>7.2f}  "
        f"validas {len(validas):>5}/{total}"
    )


def salvar_relatorio(caminho, texto):
    """Grava o relatório em UTF-8."""
    pass  # ← implemente aqui
