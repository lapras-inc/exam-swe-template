#!/usr/bin/env bash

pip install -r /app/requirements.txt
service nginx start

exec "$@"