FROM python:3.6
MAINTAINER denzow <yamada@scouty.co.jp>

EXPOSE 80
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8

WORKDIR /app

RUN pip install -v pip-tools==1.9.0 bottle

ADD . /app
