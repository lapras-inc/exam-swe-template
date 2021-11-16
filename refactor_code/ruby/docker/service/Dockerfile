FROM ruby:2.5.3-slim-stretch

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8

WORKDIR /app

RUN set -ex && \
    apt-get update && \
    apt-get install -y build-essential \
    libsqlite3-dev
