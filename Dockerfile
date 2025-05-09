FROM python:3.11-slim

WORKDIR /app

COPY ./src/ /app/src/
COPY ./config/ /app/config/
COPY requirements.txt /app
COPY main.py /app
COPY VERSION.txt /app


RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["/usr/local/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
### ENTRYPOINT [ "uvicorn", "main:app" ]




