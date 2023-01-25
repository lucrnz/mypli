# syntax=docker/dockerfile:1
FROM python:3.11-alpine3.16

# Program requirements
RUN apk add --no-cache openssh-client git

ARG USER_ID
ARG GROUP_ID

RUN mkdir -p /app && \
    addgroup --gid $GROUP_ID -S appgroup && \
    adduser --home /app --uid $USER_ID -S appuser -G appgroup && \
    chown $USER_ID:$GROUP_ID /app

USER appuser
WORKDIR /app

COPY --chown=$USER_ID:$GROUP_ID requirements.txt .
COPY --chown=$USER_ID:$GROUP_ID Dockerentry.sh .

RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

ENTRYPOINT [ "./Dockerentry.sh"]
