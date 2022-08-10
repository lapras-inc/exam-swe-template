#!/bin/bash -eu

run_type="${ISUCOUTEA_RUN_TYPE:-"run_python"}"

check_message="start application..."

figlet -f slant "ISUCOUTEA"

echo "run_type: $run_type"

echo "read rc file..."
source ~/.bashrc
echo "complete."

echo "start services..."
sudo service nginx start
sudo service mysql start
echo "complete."

echo "create database and user..."
sudo mysql -u root -pishocon << EOF
DROP DATABASE IF EXISTS scoutea;
CREATE DATABASE scoutea;

DROP USER IF EXISTS scouty;
CREATE USER IF NOT EXISTS scouty IDENTIFIED BY 'scouty';
GRANT ALL ON *.* TO scouty;
EOF
echo "complete."

echo 'import initial data to database...'
tar xOf ~/data/dbdump.tar.gz | sudo mysql -u scouty -pscouty scoutea
echo "complete."

function run_python() {
  echo "run python app..."
  cd ~/webapp/python
  poetry config virtualenvs.create false
  poetry install
  echo "$check_message"
  poetry run uwsgi app.ini
}

function run_ruby() {
  echo "run ruby app..."
  cd ~/webapp/ruby
  bundle install
  echo "$check_message"
  bundle exec puma -C config_puma.rb
}

function run_go() {
  echo "run go app..."
  cd ~/webapp/go
  go install
  go build -o /tmp/webapp
  echo "$check_message"
  /tmp/webapp
}

function run_custom() {
  echo "run custom app..."
  # ここでアプリケーションサーバの起動準備をおこなってください

  # このメッセージを標準出力に出力後、一定時間経過するとベンチマークが走り出します
  echo "$check_message"

  # ここでアプリケーションサーバの起動をおこなってください
}

"$run_type"
