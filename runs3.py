import os
from src.ingest import upload_s3, parse_s3, get_zip, unzip
from config import config
import logging
import argparse

# set up logging config
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__file__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sep',
                        default=';',
                        help="CSV separator if using pandas")
    parser.add_argument('--s3path', default='s3://2021-msia423-ko-matthew/raw/pulse2021.csv',
                        help="If used, will load data via pandas")
    parser.add_argument('--local_path', default='data/raw/pulse2021_puf_27.csv',
                        help="Where to load data to in S3")
    args = parser.parse_args()

    get_zip(config.SOURCE_URL,config.RAW_ZIP_LOCATION)

    unzip(config.RAW_ZIP_LOCATION,config.RAW_LOCATION,config.DATA_FILENAME)

    upload_s3(args.local_path, args.s3path)
