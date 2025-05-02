import jwt
import datetime
import os

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from typing import Optional
from dotenv import load_dotenv

router = APIRouter()  # Cria um router separado

# Carregar variáveis de ambiente
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "chave_secreta")
SECRET_USERNAME = os.getenv("SECRET_USERNAME", "admin")
SECRET_PWD = os.getenv("SECRET_PWD", "1234")
TIME_EXPIRES=30 #minutos

# Configuração do OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Função para criar o token JWT
def create_jwt_token(data: dict, expires_delta: Optional[int] = TIME_EXPIRES):
    print(f"Cria um token JWT válido por {TIME_EXPIRES} minutos")
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

# Rota para gerar o token JWT
@router.post("/auth/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    if username == SECRET_USERNAME and password == SECRET_PWD:
        token = create_jwt_token({"sub": username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")

# Função para verificar o token
def verify_token(token: str = Depends(oauth2_scheme)):
    """Decodifica e verifica o token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
