import auth.login as auth_login
import api.getPortal_producao as getPortal

from fastapi import Depends,FastAPI

app = FastAPI()

def getVersion() -> str:
    with open('VERSION.txt', 'r') as file:
        version = file.read().strip()
    return version

VERSION_API = getVersion()

@app.get("/version")
def get_version(user: dict = Depends(auth_login.verify_token)):
    return { "VERSION" : VERSION_API}

#Incluir a route do auth/* # fazer o token.
app.include_router(auth_login.router)

#Incluir a route do api/* # fazer a captura de dados na web.
app.include_router(getPortal.router)
