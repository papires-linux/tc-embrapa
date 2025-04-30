import src.auth.login as auth_login
import src.api.getPortal as getPortal

from fastapi import FastAPI

def getVersion() -> str:
    with open('VERSION.txt', 'r') as file:
        version = file.read().strip()
    return version

VERSION_API = getVersion()

app = FastAPI(
    title="API para coletar dados do portal embrapa",
    description="Esta é uma API para captura dados do portal embrapa e retorna na api como json.",
    version=VERSION_API,
    docs_url="/docs", 
    redoc_url="/redoc"
)

@app.get("/health")
def get_version():
    return {
        "VERSAO" : VERSION_API,
        "STATUS" : "OK"
    }

#Incluir a route do auth/* # fazer o token.
app.include_router(auth_login.router)

#Incluir a route do api/* # fazer a captura de dados na web.
app.include_router(getPortal.router)
