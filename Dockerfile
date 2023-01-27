# syntax=docker/dockerfile:1
FROM python:3.11-alpine3.16

# Program requirements
RUN apk add --no-cache openssh-client

WORKDIR /app

COPY requirements.txt .
COPY Dockerentry.sh .

RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

ENTRYPOINT [ "./Dockerentry.sh"]
