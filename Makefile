image:
				docker build -f app/Dockerfile -t vaccine_project .

db:
				docker run \
				--mount type=bind,source="$(shell pwd)",target=/app/ vaccine_project run.py create_db

raw:
				docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY \
				--mount type=bind,source="$(shell pwd)",target=/app/ vaccine_project run.py acquire

data/clean/clean.csv:
				docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY \
				--mount type=bind,source="$(shell pwd)",target=/app/ vaccine_project run.py clean

cleaned: data/clean/clean.csv

models/model.pkl: data/clean/clean.csv
				docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY \
				--mount type=bind,source="$(shell pwd)",target=/app/ \
				 vaccine_project run.py train

model: models/model.pkl

models/encoder.pkl: model

flask: models/model.pkl models/encoder.pkl
				docker run -e SQLALCHEMY_DATABASE_URI \
				--mount type=bind,source="$(shell pwd)",target=/app/ \
				-p 5000:5000 \
				vaccine_project app.py

tests:
				docker run vaccine_project -m pytest

clean:
				rm data/clean/*
				rm data/raw/*
				rm models/*

acquire: db raw

app: models/model.pkl models/encoder.pkl flask

pipeline: cleaned model

.PHONY: tests cleaned clean raw model acquire flask image pipeline app
