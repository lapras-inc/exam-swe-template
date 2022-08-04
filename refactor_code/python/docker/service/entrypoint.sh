#!/usr/bin/env bash

poetry config virtualenvs.create false
poetry install
service nginx start

echo "start application."
exec "$@"