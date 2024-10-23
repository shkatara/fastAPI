FROM python:3.10-alpine3.16
LABEL dev.orbstack.http-port=8080
WORKDIR /app
COPY requirements.txt .
COPY app /app/app
COPY database /app/database
RUN pip install -r requirements.txt && apk add curl 
EXPOSE 8080
CMD ["python3", "app/main.py"]
