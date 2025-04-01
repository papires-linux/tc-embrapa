FROM python:3.11

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expor a porta da aplicação
EXPOSE 8000

# Comando para rodar a API
CMD ["uvicorn", "auth.login:app", "--host", "0.0.0.0", "--port", "8000"]