# syntax=docker/dockerfile:1
FROM python:3.11-alpine3.16

# Program requirements
RUN apk add --no-cache openssh-client git

ARG USER_ID
ARG GROUP_ID

RUN mkdir /app && \
    addgroup --gid $GROUP_ID -S appgroup && \
    adduser --home /app --uid $USER_ID -S appuser -G appgroup && \
    chown $USER_ID:$GROUP_ID /app

USER appuser
WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "./Dockerentry.sh"]
