FROM ubuntu:22.04

ENV LANG "en_US.UTF-8"

# パッケージインストール
RUN apt-get update

RUN apt-get install -y \
    # Common packages
    wget sudo less vim git curl locales-all figlet \
    # https://github.com/rbenv/ruby-build/wiki#ubuntudebianmint
    autoconf bison build-essential libssl-dev libyaml-dev libreadline6-dev \
    zlib1g-dev libncurses5-dev libffi-dev libgdbm6 libgdbm-dev libdb-dev \
    # MySQL
    mysql-client-8.0 mysql-server-8.0 libmysqlclient-dev \
    # nginx
    nginx && \
    apt-get clean

# ユーザ作成
RUN groupadd -g 1001 scouty && \
    useradd  -g scouty -G sudo -m -s /bin/bash scouty && \
    echo "scouty:scouty" | chpasswd && \
    echo "scouty ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER scouty
WORKDIR /home/scouty

# Go のインストール
ENV GOROOT="/usr/local/go"
ENV PATH="$GOROOT/bin:$PATH"
ENV GOPATH="$HOME/.local/go"

RUN GO_VERSION="1.18.5" && \
    arch="$(dpkg --print-architecture)" && arch="${arch##*-}" && \
    wget -O go.tgz "https://go.dev/dl/go$GO_VERSION.linux-${arch}.tar.gz" && \
    sudo tar -C /usr/local -xzf go.tgz && \
    rm -f go.tgz && \
    echo "installed version: $(go version)"

# 初期データのダウンロード
RUN mkdir "data/" && \
    cd "data/" && \
    curl -O "https://s3-ap-northeast-1.amazonaws.com/scouty-sw/exam/assets/dbdump.tar.gz"

RUN sudo chmod 777 -R /var/run/
