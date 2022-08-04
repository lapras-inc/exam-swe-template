FROM python:3.9.13

EXPOSE 80
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8

WORKDIR /app

RUN apt-get update

RUN pip install --upgrade pip && \
    pip install bottle==0.12.23

ADD . /app
