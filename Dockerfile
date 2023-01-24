# syntax=docker/dockerfile:1
FROM python:3.11-alpine3.16
WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "./Dockerentry.sh"]
