import logging.config

import argparse
import os
from config import config

from src.ingest import upload_s3, get_zip, unzip
from src.createdb import create_db

logging.config.fileConfig('config/logging/local.conf')

# Add parsers for both creating a database and uploading source data to s3 bucket
parser = argparse.ArgumentParser(description="Create database or upload data to s3")
subparsers = parser.add_subparsers(dest='subparser_name')

# Sub-parser for creating a database
sb_create = subparsers.add_parser("create_db", description="Create database")

# Sub-parser for ingesting new data into s3 bucket
sb_ingest = subparsers.add_parser("ingest", description="Add data to s3 bucket")
sb_ingest.add_argument('--s3path',default='s3://2021-msia423-ko-matthew/raw/pulse2021.csv',
                    help="If used, will load data to specified path")
sb_ingest.add_argument('--local_path', default=config.RAW_CSV_LOCATION,
                    help="Where to load data to in S3")

args = parser.parse_args()
sp_used = args.subparser_name

if __name__ == '__main__':
    if sp_used == 'create_db':
        create_db()
    elif sp_used == 'ingest':
        get_zip(config.SOURCE_URL,config.RAW_ZIP_LOCATION)
        unzip(config.RAW_ZIP_LOCATION,config.RAW_LOCATION,config.DATA_FILENAME)
        upload_s3(args.local_path, args.s3path)
    else:
        parser.print_help()
