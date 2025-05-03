import logging
import requests

from typing import Optional, Any, Literal

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse

from src.auth import login as auth_login
from src.services import web_scraping as scraping

# Configuração de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Cria um router separado para os endpoints
router = APIRouter()

# Carrega arquivos de configuração
CONFIG_JSON = scraping.ler_Variaveis('config/config.json')
CONFIG_DADOS_JSON = scraping.ler_Variaveis('config/db_site.json')
DEFAULT_TAG_TB_BASE = CONFIG_JSON["DEFAULT_TAG_TB_BASE"]


#Pegar a lista funcoes
def list_funcoes() -> list[str]:
    lista = []
    for funcao in CONFIG_DADOS_JSON:
        if CONFIG_DADOS_JSON[funcao].get('CSV'):
            lista.append(funcao.lower())
    return lista

#Pegar a lista sub_funcoes
def list_sub_funcoes() -> list[str]:
    lista = []
    for funcao in CONFIG_DADOS_JSON:
        if CONFIG_DADOS_JSON[funcao].get('SCHEMA_RAW'):
            lista.append(funcao.lower())
    return lista

#Pegar a lista tipos
def list_tipos() -> list[str]:
    lista = []
    for funcao in CONFIG_DADOS_JSON:
        if CONFIG_DADOS_JSON[funcao].get('SCHEMA_RAW'):
            for tipo in CONFIG_DADOS_JSON[funcao]:
                if CONFIG_DADOS_JSON[funcao][tipo]:
                    lista.append(tipo.lower())

    # Remove duplicatas e os itens indesejados
    REMOVER = {'schema_raw', 'schema_rename'}
    lista_filtrada = list({item for item in lista if item not in REMOVER})
    return lista_filtrada


# Dependência para autenticação
def verificar_autenticacao(user: dict = Depends(auth_login.verify_token)) -> dict:
    return user

# --- Validacao de site no ar ---
def validaSiteON() -> bool:
    try:
        url = CONFIG_DADOS_JSON["URL_BASE"].get('WEB')
        request = requests.get(url)
        if request.status_code == 200:
            return True
        else:
            return False
    except:
        raise HTTPException(status_code=502, detail=f"Site indisponível para consulta: {url}")

# --- 
def obter_dados(
        funcao: str,
        tipo: str,
        ano: Optional[int] = None
    ) -> Any:
    """Busca os dados do scraping conforme função, tipo e ano"""
    try:
        validaSiteON()
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
        funcao: Literal[*list_funcoes()],
        ano: int = Query(..., description="Ano dos dados a serem consultados"),
        user: dict = Depends(verificar_autenticacao)
    ) -> JSONResponse:
    dados = obter_dados(funcao, tipo=None, ano=ano)
    return JSONResponse(content={"response": dados})

@router.get("/api/{funcao}/{tipo}")
async def get_dados_processamento(
        funcao: Literal[*list_sub_funcoes()], # type: ignore
        tipo: Literal[*list_tipos()], # type: ignore
        ano: int = Query(..., description="Ano dos dados a serem consultados"),
        user: dict = Depends(verificar_autenticacao)
    ) -> JSONResponse:
    logger.info("Requisição para dados com tipo específico")
    dados = obter_dados(funcao, tipo, ano=ano)
    return JSONResponse(content={"response": dados})
