import logging.config
import argparse
import os

import yaml
from src.acquire import upload_s3, get_zip, unzip, download_s3
from src.createdb import create_db, add_df
from src.clean import clean
from src.train import train

logging.config.fileConfig('config/logging/local.conf')

# Add parsers for both creating a database and uploading source data to s3 bucket
parser = argparse.ArgumentParser(description='Create database or upload data to s3')
parser.add_argument('--config', default='config/test.yaml',
                    help='Path to configuration file')

subparsers = parser.add_subparsers(dest='subparser_name')

# Sub-parser for creating a database
sb_create = subparsers.add_parser('create_db', description='Create database')

# Sub-parser for ingesting new data into s3 bucket
sb_ingest = subparsers.add_parser('acquire', description='Add data to s3 bucket')
sb_ingest.add_argument('--s3_raw', required=False,
                       help='Will load data to specified path',
                       default='s3://2021-msia423-ko-matthew/raw/pulse2021.csv')

# Sub-parser for cleaning raw data from s3 bucket
sb_download = subparsers.add_parser('clean',
                                    description='Download & clean data from s3 bucket')
sb_download.add_argument('--s3_raw', required=False,
                         help='Will load data from specified path',
                         default='s3://2021-msia423-ko-matthew/raw/pulse2021.csv')

# Sub-parser for training and saving model
sb_train = subparsers.add_parser('train',
                                 description='Train model / OneHotEncoder and save to s3 bucket')

args = parser.parse_args()
sp_used = args.subparser_name


if __name__ == '__main__':
    with open(args.config, "r") as f:
        y_conf = yaml.load(f, Loader=yaml.FullLoader)

    if sp_used == 'create_db':
        create_db()
        add_df(y_conf['create_db']['local_path'])
    elif sp_used == 'acquire':
        get_zip(**y_conf['acquire']['get_zip'])
        unzip(**y_conf['acquire']['unzip'])
        upload_s3(args.s3_raw, y_conf['acquire']['upload_s3']['local_path'])
    elif sp_used == 'clean':
        download_s3(args.s3_raw, **y_conf['acquire']['download_s3'])
        clean(**y_conf['clean']['clean'])
    elif sp_used == 'train':
        train(y_conf['train']['local_path'], **y_conf['train']['train'])
    else:
        parser.print_help()
