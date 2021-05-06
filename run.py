import os
from src.ingest import upload_s3, parse_s3, get_zip, unzip
from src.createdb import create_db
from config import config
import logging
import argparse

# set up logging config
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__file__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser_name')

    sb_create = subparsers.add_parser("create_db", description="Create database")
    # sb_create.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
    #                        help="SQLAlchemy connection URI for database")

    sb_ingest = subparsers.add_parser("ingest", description="Add data to database",
                                        help="Used for ingesting data into s3")

    sb_ingest.add_argument('--s3path',default='s3://2021-msia423-ko-matthew/raw/pulse2021.csv',
                        help="If used, will load data to specified path")

    sb_ingest.add_argument('--local_path', default='data/raw/pulse2021_puf_27.csv',
                        help="Where to load data to in S3")

    args = parser.parse_args()
    sp_used = args.subparser_name

    if sp_used == 'create_db':
        create_db()
    elif sp_used == 'ingest':
        get_zip(config.SOURCE_URL,config.RAW_ZIP_LOCATION)
        unzip(config.RAW_ZIP_LOCATION,config.RAW_LOCATION,config.DATA_FILENAME)
        upload_s3(args.local_path, args.s3path)
    else:
        parser.print_help()
