# syntax=docker/dockerfile:1
FROM golang:1.19-alpine as builder

RUN mkdir /build

COPY . /build
WORKDIR /build
RUN CGO_ENABLED=0 GOOS=linux go build -o main

FROM alpine:3.17
WORKDIR /app

# Grab built binary
COPY --from=builder /build/main .

# Program requirements
RUN apk add --no-cache openssh-client

COPY Dockerentry.sh .

ENTRYPOINT [ "./Dockerentry.sh"]
