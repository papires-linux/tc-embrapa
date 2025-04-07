import auth.login as auth_login
import api.web_scraping as scraping

from fastapi import APIRouter, HTTPException,Depends
from fastapi.responses import JSONResponse


router = APIRouter()  # Cria um router separado
DEFAULT_TAG_TB_BASE = "tb_base tb_dados"

ANO_MAXIMO = 2024
ANO_MINIMO = 1970

VAR_WEB_JSON = scraping.lerVariaveis('sources/url_web.json')

# Rota protegida
@router.get("/api/producao")
async def get_dados_producao(user: dict = Depends(auth_login.verify_token)):
    url = VAR_WEB_JSON["PRODUCAO"]
    dados = scraping.getDadosWebScraping(url, DEFAULT_TAG_TB_BASE) 
    return JSONResponse(
        content={"response": dados }
    )

@router.get("/api/producao/{ano}")
async def get_dados_producao(ano: int, user: dict = Depends(auth_login.verify_token)):
    url = VAR_WEB_JSON["PRODUCAO"]
    if (ANO_MINIMO > int(ano)) or (int(ano) > ANO_MAXIMO):
        raise HTTPException(
            status_code=400,
            detail=f"Ano não corresponde ao período, escolher entre {ANO_MINIMO} e {ANO_MAXIMO}."
        )
    url_com_ano = url.split("?")[0]+"?ano="+str(ano)+"&"+url.split("?")[1]
    dados = scraping.getDadosWebScraping(url_com_ano, DEFAULT_TAG_TB_BASE) 
    return JSONResponse(
        content={"response": dados }
    )



