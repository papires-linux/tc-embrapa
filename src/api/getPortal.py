import logging
from typing import Optional, Any, Dict

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse

from src.auth import login as auth_login
from src.operator import operator_enum, web_scraping as scraping

# Configuração de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Cria um router separado para os endpoints
router = APIRouter()

# Carrega arquivos de configuração
CONFIG_JSON = scraping.ler_Variaveis('config/config.json')
CONFIG_DADOS_JSON = scraping.ler_Variaveis('config/db_site.json')
DEFAULT_TAG_TB_BASE = CONFIG_JSON["DEFAULT_TAG_TB_BASE"]

# Dependência para autenticação
def verificar_autenticacao(user: dict = Depends(auth_login.verify_token)) -> dict:
    return user

def obter_dados(
    funcao: operator_enum.FuncaoEnum,
    #tipo: Optional[str] = None,
    tipo: operator_enum.TipoEnum,
    ano: Optional[int] = None
) -> Any:
    """Busca os dados do scraping conforme função, tipo e ano"""
    try:
        funcao_upper = funcao.upper()
        if tipo:
            tipo_upper = tipo.upper()
            url = CONFIG_DADOS_JSON[funcao_upper].get(tipo_upper, {}).get("WEB")
        else:
            url = CONFIG_DADOS_JSON[funcao_upper].get("WEB")

        logger.info(f"Buscando dados da URL: {url}")

        if not url:
            raise HTTPException(status_code=404, detail="Path not found")

        status, dados = scraping.get_dados_web_scraping(url, funcao, tipo, ano, DEFAULT_TAG_TB_BASE)

        if status != 200:
            raise HTTPException(status_code=status, detail=dados)

        return dados

    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Erro de configuração: {e}")

@router.get("/api/{funcao}")
async def get_dados_funcao(
    funcao: operator_enum.FuncaoEnum,
    ano: int = Query(..., description="Ano dos dados a serem consultados"),
    user: dict = Depends(verificar_autenticacao)
) -> JSONResponse:
    dados = obter_dados(funcao, ano=ano)
    return JSONResponse(content={"response": dados})

@router.get("/api/{funcao}/{tipo}")
async def get_dados_processamento(
    funcao: operator_enum.FuncaoEnum,
    #tipo: str,
    tipo: operator_enum.TipoEnum,
    ano: int = Query(..., description="Ano dos dados a serem consultados"),
    user: dict = Depends(verificar_autenticacao)
) -> JSONResponse:
    logger.info("Requisição para dados com tipo específico")
    dados = obter_dados(funcao, tipo, ano=ano)
    return JSONResponse(content={"response": dados})
