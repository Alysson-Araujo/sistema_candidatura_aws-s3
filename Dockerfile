# Etapa 1: Escolher a imagem base
FROM python:3.11-slim

WORKDIR /app

COPY . /app/

ENV AWS_BUCKET_NAME=bucket-name
ENV AWS_REGION=us-east-1 

ENV MONGODB_URI=your-mongodb-uri
ENV MONGODB_DB_NAME=your-db-name
ENV MONGODB_COLLECTION_NAME=your-collection-name

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]