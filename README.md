
#### Criar ambiente virtual e instalar dependências:
```
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt                     
pip install --upgrade pip
```


#### Executar o código: 

```
uvicorn main:app --reload
```

#### Pegar o token:
```
curl --location 'http://127.0.0.1:8000/auth/token' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'username=user' \
--data-urlencode 'password=pwd'
````




