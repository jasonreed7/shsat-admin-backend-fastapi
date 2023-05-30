import asyncio
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client("s3")

def get_s3_client():
        global s3_client
        if s3_client is None:
            s3_client = boto3.client("s3")

        return s3_client

async def upload_file(file_path: Path, bucket: str, object_name: str):
        s3_client = get_s3_client()

        def upload_file_func():
            s3_client.upload_file(file_path, bucket, object_name)

        # See https://bbc.github.io/cloudfit-public-docs/asyncio/asyncio-part-5.html
        await asyncio.to_thread(upload_file_func)