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
    ESPUMANTES = "espumantes"
    SUCO_UVA = "suco_uva"
    UVAS_FRESCAS = "uvas_frescas"
    UVAS_PASSAS = "uvas_passas"
