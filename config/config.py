from os import path

PROJECT_HOME = path.dirname(path.dirname(path.abspath(__file__)))
SOURCE_URL="https://www2.census.gov/programs-surveys/demo/datasets/hhp/2021/wk27/HPS_Week27_PUF_CSV.zip"
DATA_FILENAME="pulse2021_puf_27.csv"
RAW_ZIP_LOCATION = path.join(PROJECT_HOME,'data/raw/pulse2021.zip')
RAW_LOCATION = path.join(PROJECT_HOME,'data/raw/')
RAW_CSV_LOCATION = path.join(PROJECT_HOME,'data/raw/pulse2021_puf_27.csv')
S3_BUCKET = "raw/pulse2021.csv"
