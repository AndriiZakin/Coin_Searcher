FROM python:3.11-slim-buster AS base

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

COPY .env /app/.env

ENV PYTHONUNBUFFERED 1

CMD ["python", "src/main.py"]