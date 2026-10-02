class ErroDeSensor(Exception):
    """Exceção base para erros de validação de sensores."""


class ErroLeituraInvalida(ErroDeSensor):
    """Leitura fora da faixa esperada."""


class ErroTipoInvalido(ErroDeSensor):
    """Leitura não é um número."""


def validar_tipo(valor):
    """Verifica se o valor é numérico (int ou float). Lança ErroTipoInvalido caso não seja."""
    if not isinstance(valor, (int, float)):
        raise ErroTipoInvalido("O valor não é nem um número inteiro e nem um real")


def validar_faixa(valor, minimo=0, maximo=1000):
    """Verifica se o valor está dentro de [minimo, maximo]. Lança ErroLeituraInvalida caso não esteja."""
    if valor < minimo or valor > maximo:
        raise ErroLeituraInvalida("Fora do limite de leitura seguro")


def validar_lote(leituras, minimo=0, maximo=1000):
    """Valida uma lista de leituras. Retorna uma tupla (validas, invalidas)."""
    validas = []
    invalidas = []
    
    for leitura in leituras:
        try:
            validar_tipo(leitura)
            validar_faixa(leitura, minimo, maximo)
        except (ErroTipoInvalido, ErroLeituraInvalida):
            invalidas.append(leitura)
        else:
            validas.append(leitura)
        finally:
            print(f"Processada a leitura: {leitura}")
            
    return validas, invalidas


if __name__ == "__main__":
    print(validar_faixa(500))
    try:
        validar_faixa(-10)
    except ErroDeSensor as e:
        print(f"Erro esperado capturado: {e}")
