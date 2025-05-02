from fastapi.testclient import TestClient
from fastapi import FastAPI
from src.auth import login as auth_login

app = FastAPI()
app.include_router(auth_login.router)

client = TestClient(app)

def test_login_success():
    response = client.post("/auth/token", data={
        "username": auth_login.SECRET_USERNAME,
        "password": auth_login.SECRET_PWD
    })
    assert response.status_code == 200
    json = response.json()
    assert "access_token" in json
    assert json["token_type"] == "bearer"

def test_login_failure():
    response = client.post("/auth/token", data={
        "username": "invalido",
        "password": "errado"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Usuário ou senha incorretos"