#!/usr/bin/env bash

bundle install --path vendor/bundle

if [ -f ./db/development.sqlite3 ]; then
  RACK_ENV=development bundle exec rake db:reset
  RACK_ENV=test bundle exec rake db:seed
else
  RACK_ENV=development bundle exec rake db:create
  RACK_ENV=development bundle exec rake db:migrate
  RACK_ENV=development bundle exec rake db:seed
  RACK_ENV=test bundle exec rake db:migrate
  RACK_ENV=test bundle exec rake db:seed
fi

echo "start application."
exec "$@"
