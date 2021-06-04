import logging.config
import argparse
import os

import yaml
from config import config
from src.acquire import upload_s3, get_zip, unzip, download_s3
from src.createdb import create_db, add_df
from src.clean import clean
from src.train import train

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
sb_ingest = subparsers.add_parser('acquire', description='Add data to s3 bucket')
sb_ingest.add_argument('--s3_raw', required=True,
                       help='Will load data to specified path')

# Sub-parser for cleaning raw data from s3 bucket
sb_download = subparsers.add_parser('clean',
                                    description='Download & clean data from s3 bucket')
sb_download.add_argument('--s3_raw', required=False,
                         help='Will load data from specified path')
sb_download.add_argument('--s3_clean', required=False,
                         help='Will load clean data to specified path')

# Sub-parser for training and saving model
sb_train = subparsers.add_parser('train',
                                 description='Train model / OneHotEncoder and save to s3 bucket')
sb_train.add_argument('--s3_clean', required=False,
                      help='Will load data from specified path')
sb_train.add_argument('--s3_model', required=False,
                      help='Will upload model to path')
sb_train.add_argument('--s3_enc', required=False,
                      help='Will upload OneHotEncoder to path')
sb_train.add_argument('--s3_results', required=False,
                      help='Will upload model results file to path')

args = parser.parse_args()
sp_used = args.subparser_name


if __name__ == '__main__':

    with open(args.config, "r") as f:
        y_conf = yaml.load(f, Loader=yaml.FullLoader)

    if sp_used == 'create_db':
        create_db()
    elif sp_used == 'acquire':
        if args.s3_raw:
            get_zip(**y_conf['acquire']['get_zip'])
            unzip(**y_conf['acquire']['unzip'])
            upload_s3(args.s3_raw, y_conf['acquire']['upload_s3']['local_path'])
        else:
            get_zip(**y_conf['ingest']['get_zip'])
            unzip(**y_conf['ingest']['unzip'])
    elif sp_used == 'clean':
        if args.s3_raw:
            download_s3(args.s3_raw, **y_conf['acquire']['download_s3'])
            clean(**y_conf['clean']['clean'])
            upload_s3(args.s3_clean, y_conf['clean']['clean']['save_path'])
        else:
            clean(**y_conf['clean']['clean'])
    elif sp_used == 'train':
        if args.s3_clean:
            download_s3(args.s3_clean, y_conf['train']['local_path'],
                        y_conf['train']['sep'])
            train(y_conf['train']['local_path'], **y_conf['train']['train'])
            upload_s3(args.s3_model, y_conf['train']['train']['model_path'])
            upload_s3(args.s3_enc, y_conf['train']['train']['encoder_path'])
            upload_s3(args.s3_results, y_conf['train']['train']['results_path'])
        else:
            train(y_conf['train']['local_path'], **y_conf['train']['train'])
    else:
        parser.print_help()
