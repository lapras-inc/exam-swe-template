Python実装固有の説明
=============


#### appコンテナについて

`app`コンテナではFlaskとnginxが起動します。ホストOS上の`http://localhost:80/`から本サービスにアクセスできます。Flaskはuwsgiで動作しており、コードを変更するとオートリロードします。リロード時には、`admin/create_db.py`が実行され各モデルは初期化されます。初期データとして`testuser/testuser`というアカウントと20種類の茶葉データがあるのでこちらを利用して開発してください。必要に応じて初期データは変更して構いません。

#### アプリケーションフレームワークについて

[Flask](http://flask.pocoo.org/) + [Flask-login](https://flask-login.readthedocs.io/en/latest/)を使用しています。ORMには[peewee](http://docs.peewee-orm.com/en/latest/index.html)を使用しています。


#### バックエンドDBについて

`/var/lib/data/refactea.db`というsqlite3を使用しています。

#### unittestについて

`app`コンテナ内で以下の手順にてunittestを実行することができます。

```
$ cd /app/application
$ python test.py
```
