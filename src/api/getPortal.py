import logging

import src.auth.login as auth_login
import src.lib.operator as operator
import src.lib.web_scraping as scraping
from fastapi import APIRouter, HTTPException, Depends, Path
from fastapi.responses import JSONResponse

router = APIRouter()  # Cria um router separado
CONFIG_JSON = scraping.lerVariaveis('config/config.json')
CONFIG_DADOS_JSON = scraping.lerVariaveis('config/db_site.json')

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

# Dependência para autenticação
def verificar_autenticacao(user: dict = Depends(auth_login.verify_token)):
    return user

# Função para buscar dados de produção
def obter_dados(funcao: operator.FuncaoEnum, tipo: str = None, ano: int = None):
    if CONFIG_DADOS_JSON[funcao.upper()].get(tipo.upper()) is None:
        url = None
    else:
        url = CONFIG_DADOS_JSON[funcao.upper()].get(tipo.upper()).get("WEB")
    
    status, dados = scraping.getDadosWebScraping(funcao, tipo, ano,DEFAULT_TAG_TB_BASE)
    if status != 200:
        raise HTTPException(
            status_code=status,
            detail=dados
        )
    return dados

@router.get("/api/{funcao}")
@verificar_autenticacao
async def get_dados_funcao(
        funcao: operator.FuncaoEnum
    ):
    echo("get_dados_funcao")
    dados = obter_dados(funcao)
    return JSONResponse(content={"response": dados})

@router.get("/api/{funcao}/{tipo}")
@verificar_autenticacao
async def get_dados_processamento(
        funcao: operator.FuncaoEnum,
        tipo: str
    ):
    echo("get_dados_processamento")
    dados = obter_dados(funcao,tipo)
    return JSONResponse(content={"response": dados})

@router.get("/api/{funcao}/{tipo}/{ano}")
@verificar_autenticacao
async def get_dados_processamento_com_ano(
        funcao: str,
        tipo: str,
        ano: int = Path(ge=ANO_MINIMO,le=ANO_MAXIMO)
    ):
    echo("get_dados_processamento_com_ano")
    validar_ano(ano)  # Valida o ano
    dados = obter_dados(funcao,tipo, ano)
    return JSONResponse(content={"response": dados})

