#!/bin/bash -eu

cd /benchmark
pip install -r requirements.txt > /dev/null 2>&1

python benchmark.py
