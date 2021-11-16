#!/usr/bin/env bash

bundle install --path vendor/bundle
RACK_ENV=development bundle exec rake db:create
RACK_ENV=development bundle exec rake db:migrate
RACK_ENV=development bundle exec rake db:seed

exec "$@"
