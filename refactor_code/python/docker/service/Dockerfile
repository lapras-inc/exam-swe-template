
FROM python:3.6.6-jessie

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8

WORKDIR /app

# Nginx のインストール
RUN wget http://nginx.org/keys/nginx_signing.key
RUN apt-key add nginx_signing.key
RUN echo deb http://nginx.org/packages/debian/ jessie nginx >> /etc/apt/sources.list.d/Nginx.list
RUN echo deb-src http://nginx.org/packages/debian/ jessie nginx >> /etc/apt/sources.list.d/Nginx.list
RUN apt-get update
RUN apt-get install -y nginx

ADD ./nginx.conf /etc/nginx/nginx.conf

ENTRYPOINT ["docker/service/entrypoint.sh"]
