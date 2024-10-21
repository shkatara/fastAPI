FROM python:3.10-alpine3.16
WORKDIR /app
COPY requirements.txt .
COPY app /app/app
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python3", "app/main.py"]
