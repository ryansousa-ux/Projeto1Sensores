"""Leitura do CSV de estação automática do INMET — Projeto 1, Técnicas de Programação.

Formato do arquivo (dados históricos do INMET):
- encoding latin-1 (não é UTF-8!)
- 8 linhas de metadados no topo ("ESTACAO:;SAO LUIS")
- depois, uma linha de cabeçalho e uma linha por hora, separadas por ";"
"""

import csv

LINHAS_METADADOS = 8
ENCODING = "latin-1"

# Apelido curto -> nome exato da coluna no CSV do INMET
COLUNAS = {
    "temperatura": "TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)",
    "umidade": "UMIDADE RELATIVA DO AR, HORARIA (%)",
    "chuva": "PRECIPITAÇÃO TOTAL, HORÁRIO (mm)",
    "vento": "VENTO, VELOCIDADE HORARIA (m/s)",
}


class ErroFormatoArquivo(Exception):
    """O arquivo existe, mas não tem o formato esperado do INMET."""


def ler_metadados(caminho):
    """Lê as 8 primeiras linhas e retorna um dicionário.

    Ex.: {"REGIAO": "NE", "UF": "MA", "ESTACAO": "SAO LUIS", "CODIGO (WMO)": "A203", ...}
    Lança ErroFormatoArquivo se alguma dessas linhas não tiver o formato "CHAVE:;valor".
    """
    pass  # ← implemente aqui


def ler_registros(caminho):
    """Retorna a lista de registros horários; cada registro é um dicionário coluna -> texto.

    Os valores continuam como TEXTO (a conversão é papel do módulo validadores).
    Lança ErroFormatoArquivo se faltar no cabeçalho alguma coluna de COLUNAS.
    """
    pass  # ← implemente aqui


def extrair_coluna(registros, apelido):
    """Retorna a lista de textos de uma coluna, a partir do apelido ("temperatura", ...).

    Lança KeyError se o apelido não existir em COLUNAS.
    """
    pass  # ← implemente aqui


def agrupar_por_mes(registros, apelido):
    """Retorna um dicionário "AAAA/MM" -> lista de textos daquela coluna, em ordem de mês.

    A data vem na coluna "Data" no formato "2025/01/31".
    """
    pass  # ← implemente aqui
