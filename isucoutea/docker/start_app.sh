#!/bin/bash
sudo service nginx start
sudo service mysql start
sudo chown -R mysql:mysql /var/lib/mysql /var/run/mysqld
sudo service mysql start  # 正しく起動
sudo mysql -u root -pishocon -e 'CREATE DATABASE IF NOT EXISTS scoutea;' && \
sudo mysql -u root -pishocon -e "CREATE USER IF NOT EXISTS scouty IDENTIFIED BY 'scouty';" && \
sudo mysql -u root -pishocon -e 'GRANT ALL ON *.* TO scouty;' && \
cd ~/data && wget https://s3-ap-northeast-1.amazonaws.com/scouty-sw/exam/assets/dbdump.tar.gz && \
echo 'import initial data to database.....' && \
tar -zxvf dbdump.tar.gz && sudo mysql -u scouty -pscouty scoutea < ~/data/dbdump

echo 'SETUP COMPLETED !'
tail -f /dev/null
