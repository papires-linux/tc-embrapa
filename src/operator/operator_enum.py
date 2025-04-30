""""
Classes para definir os paths permitidos e a relacao com o json de configuracao
"""

from enum import Enum

class FuncaoEnum(str, Enum):
    PRODUCAO = "producao"
    PROCESSAMENTO = "processamento"
    COMERCIALIZACAO = "comercializacao"
    IMPORTACAO = "importacao"
    EXPORTACAO = "exportacao"

class TipoEnum(str,Enum):
    # processamento
    VINIFERAS = "viniferas"
    AMERICANAS_HIBRIDAS = "americanas_hibridas"
    UVAS_MESA = "uvas_mesa"
    SEM_CLASSIFICACAO = "sem_classificacao"

    # importacao/exportacao
    VINHOS_MESA = "vinhos_mesa"
    ESPUMANTES = "espumantes"
    SUCO_UVA = "suco_uva"
    UVAS_FRESCAS = "uvas_frescas"
    UVAS_PASSAS = "uvas_passas"