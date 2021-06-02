import logging.config
import argparse
import os

import yaml
from config import config
from src.ingest import upload_s3, get_zip, unzip, download_s3
from src.createdb import create_db, add_df
from src.clean import clean

logging.config.fileConfig('config/logging/local.conf')

source_url = config.SOURCE_URL  # url cotaining data for application
zip_loc = config.RAW_ZIP_LOCATION  # path to zip file downloaded
raw_directory = config.RAW_LOCATION  # Directory of zip file, for unzip function
file_name = config.DATA_FILENAME  # File to extract within zip
csv_loc = config.RAW_CSV_LOCATION  # Path to csv that was extracted

# Add parsers for both creating a database and uploading source data to s3 bucket
parser = argparse.ArgumentParser(description='Create database or upload data to s3')
parser.add_argument('--config', default='config/test.yaml',
                        help='Path to configuration file')

subparsers = parser.add_subparsers(dest='subparser_name')

# Sub-parser for creating a database
sb_create = subparsers.add_parser('create_db', description='Create database')

# Sub-parser for ingesting new data into s3 bucket
sb_ingest = subparsers.add_parser('ingest', description='Add data to s3 bucket')
sb_ingest.add_argument('--s3path', required=True,
                       help='Will load data to specified path')

# Sub-parser for downloading data from s3 bucket
sb_download = subparsers.add_parser('clean',
                                    description='Download & clean data from s3 bucket')
sb_download.add_argument('--s3path', required=True,
                         help='Will load data from specified path')

args = parser.parse_args()
sp_used = args.subparser_name

if __name__ == '__main__':

    with open(args.config, "r") as f:
        y_conf = yaml.load(f, Loader=yaml.FullLoader)

    if sp_used == 'create_db':
        create_db()
    elif sp_used == 'ingest':
        get_zip(**y_conf['ingest']['get_zip'])
        unzip(**y_conf['ingest']['unzip'])
        upload_s3(args.s3path, y_conf['ingest']['upload_s3']['local_path'])
    elif sp_used == 'clean':
        download_s3(args.s3path, **y_conf['ingest']['download_s3'])
        output = clean(**y_conf['clean']['clean'])
        add_df(output)
    else:
        parser.print_help()
