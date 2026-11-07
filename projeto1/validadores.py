"""Validação de leituras de sensores — Projeto 1, Técnicas de Programação.

Converte o texto bruto que vem do CSV do INMET em número e confere se a leitura
é fisicamente plausível. Cada problema vira uma exceção própria, para que quem
chama saiba exatamente o que deu errado.
"""


class ErroDeSensor(Exception):
    """Exceção base para erros de validação de sensores."""


class ErroCampoAusente(ErroDeSensor):
    """O sensor não registrou valor naquela hora (campo vazio no CSV)."""


class ErroTipoInvalido(ErroDeSensor):
    """A leitura não é um número."""


class ErroLeituraInvalida(ErroDeSensor):
    """A leitura é um número, mas está fora da faixa plausível."""


def validar_tipo(item):
    if type(item) is bool:
        raise ErroTipoInvalido("Booleanos não são permitidos")
    
    if type(item) not in (int, float):
        raise ErroTipoInvalido("Tipo de dado não suportado")


def validar_faixa(valor, minimo=0, maximo=1000):
    """Verifica se o valor está dentro de [minimo, maximo]. Lança ErroLeituraInvalida caso não esteja."""
    valor = converter_leitura(valor)
    if valor < minimo or valor > maximo:
        raise ErroLeituraInvalida("Valor fora da faixa permitida")

    return valor


def converter_leitura(leitura):
    if type(leitura) in (int, float):
        return leitura

    texto_limpo = leitura.strip()

    if not texto_limpo:
        raise ErroCampoAusente("Campo vazio")

    texto_com_ponto = texto_limpo.replace(',', '.')

    try:
        return float(texto_com_ponto)
    except ValueError:
        raise ErroTipoInvalido("Valor não numérico")


def validar_lote(leituras, minimo=0, maximo=1000):
    """Valida uma lista de leituras e retorna a tupla (validas, invalidas).

    - Cada leitura pode ser número ou texto; texto passa antes por converter_leitura.
    - validas: lista de floats/ints que passaram em todas as validações.
    - invalidas: lista de tuplas (leitura_original, nome_da_excecao).
      Ex.: ("", "ErroCampoAusente"), (1200, "ErroLeituraInvalida")
    """
    valores_validos = []
    valores_invalidos = []


    for item in leituras:
        try:
            valor_convertido = converter_leitura(item)
            validar_tipo(valor_convertido)
            validar_faixa(valor_convertido, minimo, maximo)
            valores_validos.append(valor_convertido)
        except ErroDeSensor as e:
            nome_erro = type(e).__name__
            valores_invalidos.append((item, nome_erro))

    return valores_validos, valores_invalidos
