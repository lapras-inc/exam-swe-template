#!/usr/bin/env puma

workers 1
pidfile './puma.pid'
bind "tcp://0.0.0.0:8080"
preload_app!
worker_timeout 60
