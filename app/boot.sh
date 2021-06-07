#!/usr/bin/env bash

#python3 run.py create_db
#python3 run.py acquire #--s3_raw s3://2021-msia423-ko-matthew/raw/pulse2021.csv
python3 run.py clean #--s3_raw s3://2021-msia423-ko-matthew/raw/pulse2021.csv --s3_clean s3://2021-msia423-ko-matthew/clean/clean.csv
python3 run.py train #--s3_clean s3://2021-msia423-ko-matthew/clean/clean.csv --s3_enc s3://2021-msia423-ko-matthew/model/encoder.pkl --s3_model s3://2021-msia423-ko-matthew/model/model.pkl --s3_results s3://2021-msia423-ko-matthew/model/results.yaml
python3 app.py
