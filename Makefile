image:
				docker build -f app/Dockerfile -t vaccine_project_mjk3551 .

db:
				docker run \
				--mount type=bind,source="$(shell pwd)",target=/app/ vaccine_project_mjk3551 run.py create_db

raw:
				docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY \
				--mount type=bind,source="$(shell pwd)",target=/app/ vaccine_project_mjk3551 run.py acquire \
				--s3_raw s3://2021-msia423-ko-matthew/raw/pulse2021.csv

data/clean/clean.csv:
				docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY \
				--mount type=bind,source="$(shell pwd)",target=/app/ vaccine_project_mjk3551 run.py clean \
				--s3_raw s3://2021-msia423-ko-matthew/raw/pulse2021.csv

clean: data/clean/clean.csv

models/model.pkl: data/clean/clean.csv
				docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY \
				--mount type=bind,source="$(shell pwd)",target=/app/ \
				 vaccine_project_mjk3551 run.py train \
				--s3_clean s3://2021-msia423-ko-matthew/clean/clean.csv

model: models/model.pkl

models/encoder.pkl: model

flask: models/model.pkl models/encoder.pkl
				docker run -e SQLALCHEMY_DATABASE_URI \
				--mount type=bind,source="$(shell pwd)",target=/app/ \
				-p 5000:5000 \
				vaccine_project_mjk3551 app.py

tests:
				docker run vaccine_project_mjk3551 -m pytest

acquire: db raw

app: data/clean/clean.csv models/model.pkl models/encoder.pkl flask

pipeline: clean model

.PHONY: tests clean all raw model acquire app flask image pipeline data/clean/clean.csv models/model.pkl
