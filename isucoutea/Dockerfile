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

# Ruby のインストール
ENV PATH="/home/scouty/.rbenv/bin:$PATH"

RUN RUBY_VERSION="3.1.2" && \
    BUNDLER_VERSION="2.3.19" && \
    wget "https://raw.githubusercontent.com/rbenv/rbenv-installer/main/bin/rbenv-installer" && \
    cat rbenv-installer | bash && \
    rm -f rbenv-installer && \
    eval "$(rbenv init -)" && \
    rbenv install "$RUBY_VERSION" && \
    rbenv global "$RUBY_VERSION" && \
    gem update --system && \
    gem install bundler -v "$BUNDLER_VERSION" && \
    echo "installed version: $(ruby -v)"

# Python のインストール
ENV PYENV_ROOT="/home/scouty/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PATH"

RUN PYTHON_VERSION="3.9.13" && \
    POETRY_VERSION="1.1.6" && \
    git clone "https://github.com/pyenv/pyenv.git" ~/.pyenv && \
    # https://uwsgi-docs.readthedocs.io/en/latest/Install.html
    sudo apt-get install -y python3-dev && \
    eval "$(pyenv init -)" && \
    eval "$(pyenv init --path)" && \
    pyenv install "$PYTHON_VERSION" && \
    pyenv global "$PYTHON_VERSION" && \
    pip install --upgrade pip && \
    pip install poetry=="$POETRY_VERSION" && \
    echo "installed version: $(python -V)"

# Go のインストール
ENV GOROOT="/usr/local/go"
ENV PATH="$GOROOT/bin:$PATH"
ENV GOPATH="$HOME/.local/go"

RUN GO_VERSION="1.18.5" && \
    wget -O go.tgz "https://go.dev/dl/go$GO_VERSION.linux-amd64.tar.gz" && \
    sudo tar -C /usr/local -xzf go.tgz && \
    rm -f go.tgz && \
    echo "installed version: $(go version)"

# 初期データのダウンロード
RUN mkdir "data/" && \
    cd "data/" && \
    curl -O "https://s3-ap-northeast-1.amazonaws.com/scouty-sw/exam/assets/dbdump.tar.gz"

COPY --chown=scouty:scouty admin/config/bashrc /home/scouty/.bashrc

RUN sudo chmod 777 -R /var/run/
