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
        file_name (str): the location and name of file that will be downloaded as path
    Returns:
        None
    '''
    try:
        with open(file_name, "wb") as f:
            r = requests.get(url, stream=True)
            f.write(r.content)
        logger.info("Zip file successfully downloaded from source, placed in %s",file_name)
    except:
        logger.error("File was unable to be downloaded from source location")

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
            zipObj.extract(data_filename,destination_path)
        logger.info("File successfully unzipped and extracted, located at %s",destination_path)
    except:
        logger.error("File %s was not able to be unzipped", source_path)

def parse_s3(s3path):
    '''Parses string to extract bucket name and s3 path
    Args:
        s3path (str): full s3 path
    Returns:
        s3bucket (str): name of s3 bucket
        s3path (str): directory path within s3 bucket
    '''
    regex = r"s3://([\w._-]+)/([\w./_-]+)"

    m = re.match(regex, s3path)
    s3bucket = m.group(1)
    s3path = m.group(2)

    return s3bucket, s3path


def upload_s3(local_path, s3path):
    '''Uploads file to s3 Bucket
    Args:
        local_path (str): the filepath of file that will be uploaded
        s3path (str): the path where the file will be located on s3
    Returns:
        None
    '''

    session = boto3.Session(aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY'))
    client = session.client('s3')

    s3bucket, s3_just_path = parse_s3(s3path)

    # s3 = boto3.resource("s3")
    # bucket = s3.Bucket(s3bucket)

    try:
        response = client.upload_file(local_path, s3bucket, s3_just_path)
        # bucket.upload_file(local_path, s3_just_path)
    except botocore.exceptions.NoCredentialsError:
        logger.error('Please provide AWS credentials via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env variables.')
    else:
        logger.info('Data successfully uploaded from %s to %s', local_path, s3path)