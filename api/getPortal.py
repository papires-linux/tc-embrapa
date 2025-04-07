import auth.login as auth_login
import lib.web_scraping as scraping
import logging
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

router = APIRouter()  # Cria um router separado
CONFIG_JSON = scraping.lerVariaveis('sources/config.json')
CONFIG_DADOS_JSON = scraping.lerVariaveis('sources/config_db_site.json')

DEFAULT_TAG_TB_BASE = CONFIG_JSON["DEFAULT_TAG_TB_BASE"]
ANO_MAXIMO = CONFIG_JSON["ANO_MAXIMO"]
ANO_MINIMO = CONFIG_JSON["ANO_MINIMO"]

def echo(texto):
    logging.info(texto)
    print(texto)
    return texto

# Função para validação do ano
def validar_ano(ano: int):
    if ANO_MINIMO > ano or ano > ANO_MAXIMO:
        raise HTTPException(
            status_code=400,
            detail=f"Ano não corresponde ao período, escolher entre {ANO_MINIMO} e {ANO_MAXIMO}."
        )

# Função para buscar dados de produção
def obter_dados(funcao: str, tipo: str, ano: int = None):
    url = CONFIG_DADOS_JSON[funcao.upper()].get(tipo.upper()).get("WEB")
    echo(f"URL para consultar o site: {url}")
    if not url:
        raise HTTPException(status_code=404, detail=f"Tipo de processamento {tipo} não encontrado.")
    dados = scraping.getDadosWebScraping(funcao, tipo, ano,DEFAULT_TAG_TB_BASE)
    return dados

# Dependência para autenticação
def verificar_autenticacao(user: dict = Depends(auth_login.verify_token)):
    return user

# Rota para processamento por tipo e ano (caso ano seja fornecido)
@router.get("/api/{funcao}/{tipo}")
async def get_dados_processamento(funcao: str,tipo: str, user: dict = Depends(verificar_autenticacao)):
    dados = obter_dados(funcao,tipo)
    return JSONResponse(content={"response": dados})

@router.get("/api/{funcao}/{tipo}/{ano}")
async def get_dados_processamento_com_ano(funcao: str,tipo: str, ano: int, user: dict = Depends(verificar_autenticacao)):
    validar_ano(ano)  # Valida o ano
    dados = obter_dados(funcao,tipo, ano)
    return JSONResponse(content={"response": dados})

