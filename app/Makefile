image:
				docker build -f app/Dockerfile -t vaccine_project .

raw:
				docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="$(shell pwd)",target=/app/ vaccine_project run.py ingest --s3path {your_s3_path}
