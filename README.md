

#### Executar o código: 

```
uvicorn auth.login:app --reload
```

#### Pegar o token:
```
curl --location 'http://127.0.0.1:8000/auth/token' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'username=user' \
--data-urlencode 'password=pwd'
````




