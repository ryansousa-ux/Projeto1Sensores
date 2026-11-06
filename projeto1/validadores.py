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


def converter_leitura(texto):
    """Converte o texto de um campo do CSV em float.

    O INMET usa vírgula como separador decimal ("27,5" -> 27.5).
    - campo vazio (ou só espaços)  -> lança ErroCampoAusente
    - texto que não é número       -> lança ErroTipoInvalido
    """
    if not texto or not texto.strip():
        raise ErroCampoAusente("Campo vazio")
    
    texto_ajustado = texto.replace(",", ".")
    
    try:
        return float(texto_ajustado)
    except ValueError:
        raise ErroTipoInvalido("O valor não é um número válido")


def validar_tipo(valor):
    """Verifica se o valor é numérico (int ou float). Lança ErroTipoInvalido caso não seja.

    Atenção: bool é subclasse de int em Python, mas True não é leitura de sensor.
    """
    pass  # ← implemente aqui


def validar_faixa(valor, minimo=0, maximo=1000):
    """Verifica se o valor está dentro de [minimo, maximo]. Lança ErroLeituraInvalida caso não esteja."""
    pass  # ← implemente aqui


def validar_lote(leituras, minimo=0, maximo=1000):
    """Valida uma lista de leituras e retorna a tupla (validas, invalidas).

    - Cada leitura pode ser número ou texto; texto passa antes por converter_leitura.
    - validas: lista de floats/ints que passaram em todas as validações.
    - invalidas: lista de tuplas (leitura_original, nome_da_excecao).
      Ex.: ("", "ErroCampoAusente"), (1200, "ErroLeituraInvalida")
    """
    pass  # ← implemente aqui
