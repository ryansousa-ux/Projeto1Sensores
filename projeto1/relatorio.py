"""Estatísticas e relatório em texto - Projeto 1, Técnicas de Programação."""

def resumir(valores):
    """Retorna {"minimo", "maximo", "media", "soma"} de uma lista de números.

    Lista vazia NÃO é erro de programa: é um sensor que não mediu nada no período.
    Nesse caso, retorna None.
    """
    if not valores:
        return None

    minimo = min(valores)
    maximo = max(valores)
    soma = sum(valores)
    media = round(soma / len(valores), 2)

    return {
        "minimo": minimo,
        "maximo": maximo,
        "media": media,
        "soma": soma
    }


def contar_motivos(invalidas):
    contagem = {}
    for leitura, motivo in invalidas:
        if motivo in contagem:
            contagem[motivo] += 1
        else:
            contagem[motivo] = 1
    return contagem


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
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(texto)