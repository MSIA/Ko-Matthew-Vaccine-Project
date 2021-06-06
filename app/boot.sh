#!/usr/bin/env bash

python3 run.py create_db
python3 run.py acquire
python3 run.py clean
python3 run.py train
python3 app.py
