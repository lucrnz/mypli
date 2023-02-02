# syntax=docker/dockerfile:1
FROM golang:1.20-alpine as builder

RUN mkdir /build

COPY . /build
WORKDIR /build
RUN CGO_ENABLED=0 GOOS=linux go build -o mypli

FROM alpine:3.17
WORKDIR /app

# Grab built binary
COPY --from=builder /build/mypli /usr/bin/mypli

# Program requirements
RUN apk add --no-cache openssh-client

COPY Dockerentry.sh .

ENTRYPOINT [ "./Dockerentry.sh"]
