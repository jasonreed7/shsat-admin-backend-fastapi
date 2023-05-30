import logging
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client("s3")

def get_s3_client():
        global s3_client
        if s3_client is None:
            s3_client = boto3.client("s3")

        return s3_client

def upload_file(file_path: Path, bucket: str, object_name: str) -> bool:
        s3_client = get_s3_client()

        try:
            s3_client.upload_file(file_path, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        
        return True