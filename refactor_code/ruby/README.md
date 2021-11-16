Ruby実装固有の説明
===========

#### appコンテナについて

`app`コンテナではSinatraが起動します。ホストOS上の`http://localhost:80/`から本サービスにアクセスできます。Sinatraはdevelopmentモードで起動してあれば、コードを変更するとオートリロードします。初期データとして`testuser/testuser`というアカウントと20種類の茶葉データを`db/seeds.rb` により追加しています。こちらを利用して開発してください。必要に応じて初期データは変更して構いません。

#### アプリケーションフレームワークについて

[Sinatra](http://sinatrarb.com/)を使用しています。ORMにはActiveRecordを、認証には[Authlogic](https://github.com/binarylogic/authlogic)使用しています。


#### バックエンドDBについて
`/app/db/development.sqlite3` というsqlite3を使用しています。

#### unittestについて

`app`コンテナ内で以下の手順にてunittestを実行することができます。

```
$ cd /app
$ bundle exec rake test
```
