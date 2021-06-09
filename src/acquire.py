import logging.config
import os
import re

import requests
import boto3
import botocore
import pandas as pd
from botocore.exceptions import ClientError
from zipfile import ZipFile

logger = logging.getLogger(__name__)

aws_id = os.environ.get('AWS_ACCESS_KEY_ID')  # AWS ID as environment variable
aws_key = os.environ.get('AWS_SECRET_ACCESS_KEY')  # AWS Key as environment variable


def get_zip(url, file_name):
    '''Downloads a file and writes it to current directory

    Args:
        url (str): the url to the file to be downloaded
        file_name (str): the location and name of file that will be downloaded as path

    Returns:
        None
    '''
    try:
        with open(file_name, "wb") as f:
            r = requests.get(url, stream=True, timeout=30)
            f.write(r.content)
        logger.info('Zip file successfully downloaded from source, placed in %s', file_name)
    except requests.ConnectionError:
        logger.error('Could not download: Connection error')
    except requests.Timeout:
        logger.error('Could not download: Timeout error')
    except Exception:
        logger.error('General: File was unable to be downloaded from source location')


def unzip(source_path, destination_path, data_filename):
    '''Unzips a zip file

    Args:
        source_path (str): the filepath of the zip file
        destination_path (str): the directory to unzip file to
        data_filename (str): the file within the zip file to extract

    Returns:
        None
    '''
    try:
        with ZipFile(source_path, 'r') as zipObj:
            zipObj.extract(data_filename, destination_path)
        logger.info('File successfully unzipped and extracted, located at %s', destination_path)
    except:
        logger.error('File %s was not able to be unzipped', source_path)


def parse_s3(s3path):
    '''Parses string to extract bucket name and s3 path

    Args:
        s3path (str): full s3 path

    Returns:
        s3bucket (str): name of s3 bucket
        s3path (str): directory path within s3 bucket
    '''
    regex = r"s3://([\w._-]+)/([\w./_-]+)"

    matched = re.match(regex, s3path)  # matched groups based on regex string
    s3bucket = matched.group(1)
    s3path = matched.group(2)

    return s3bucket, s3path


def upload_s3(s3path, local_path):
    '''Uploads file to s3 Bucket

    Args:
        local_path (str): the filepath location of file that will be uploaded
        s3path (str): the path where the file will be located on s3

    Returns:
        None
    '''
    session = boto3.Session(aws_access_key_id=aws_id,
                            aws_secret_access_key=aws_key)
    client = session.client('s3')
    s3bucket, s3_just_path = parse_s3(s3path)

    try:
        response = client.upload_file(local_path, s3bucket, s3_just_path)
    except botocore.exceptions.NoCredentialsError:
        logger.error('Please provide AWS credentials via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env variables.')
    except boto3.exceptions.S3UploadFailedError:
        logger.error("Please provide a valid S3 bucket name.")
    else:
        logger.info('Data successfully uploaded from %s to %s', local_path, s3path)


def download_s3(s3path, local_path, sep):
    '''Downloads file from S3

    Args:
        local_path (str): the filepath location of file that will be downloaded to
        s3path (str): the path where the file will be located on s3
        sep (str): separator for downloaded file

    Returns:
        None
    '''
    try:
        df = pd.read_csv(s3path, sep=sep)
    except botocore.exceptions.NoCredentialsError:
        logger.error('Please provide AWS credentials via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env variables.')
    else:
        df.to_csv(local_path, sep=sep, index=False)
        logger.info('Data downloaded from %s to %s', s3path, local_path)
