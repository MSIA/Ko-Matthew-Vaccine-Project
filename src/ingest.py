import os
import requests
import logging
import boto3
import botocore
from botocore.exceptions import ClientError
import argparse
import re
from zipfile import ZipFile

logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.ERROR)
logging.getLogger("s3transfer").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("boto3").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.getLogger("aiobotocore").setLevel(logging.ERROR)
logging.getLogger("s3fs").setLevel(logging.ERROR)


logger = logging.getLogger('s3')

def get_zip(url,file_name):
    '''Downloads a file and writes it to current directory

    Args:
        url (str): the url to the file to be downloaded
    Returns:
        None
    '''

    with open(file_name, "wb") as f:
        r = requests.get(url, stream=True)
        f.write(r.content)

def unzip(source_path, destination_path, data_filename):
    '''Unzips a zip file
    Args:
        source_filepath (str): the filepath of the zip file
        dest_filepath (str): the filepath of the unzipped file
        block_size (int): blocks to read
    Returns:
        None
    '''

    with ZipFile(source_path, 'r') as zipObj:
        zipObj.extract(data_filename,destination_path)

def parse_s3(s3path):
    regex = r"s3://([\w._-]+)/([\w./_-]+)"

    m = re.match(regex, s3path)
    s3bucket = m.group(1)
    s3path = m.group(2)

    return s3bucket, s3path


def upload_s3(local_path, s3path):

    s3bucket, s3_just_path = parse_s3(s3path)

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(s3bucket)

    try:
        bucket.upload_file(local_path, s3_just_path)
    except botocore.exceptions.NoCredentialsError:
        logger.error('Please provide AWS credentials via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env variables.')
    else:
        logger.info('Data uploaded from %s to %s', local_path, s3path)
