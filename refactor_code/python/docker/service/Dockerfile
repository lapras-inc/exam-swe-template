FROM python:3.9.13

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8

WORKDIR /app

# Nginx のインストール
RUN apt-get update
RUN apt-get install -y nginx
ADD ./nginx.conf /etc/nginx/nginx.conf

# Poetry のインストール
RUN pip install --upgrade pip && \
    pip install poetry=="1.1.6"

RUN mkdir -p /var/lib/data

ENTRYPOINT ["docker/service/entrypoint.sh"]
