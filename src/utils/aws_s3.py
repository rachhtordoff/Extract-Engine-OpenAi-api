# aws_service.py
import boto3
from botocore.client import Config as aws_config
from src.config import Config as conf
import os


class AWSService:
    def __init__(self):
        self.client = boto3.client(
            's3',
            aws_access_key_id=conf.aws_access_key_id,
            aws_secret_access_key=conf.aws_secret_access_key,
            config=aws_config(signature_version='s3v4'),
            region_name='eu-west-2'
        )

    def download_file(self, folder_id, doc_name):
        bucket_name = f'{conf.BUCKET_ID}'
        newdoc_name = f'{conf.BUCKET_NAME}/uploads/{folder_id}/{doc_name}'

        split_name = doc_name.split('/')[-1]
        documents_dir = '/opt/src/documents/'
        copy_doc_name = os.path.join(documents_dir, split_name)

        if not os.path.exists(documents_dir):
            os.makedirs(documents_dir)

        try:
            self.client.download_file(bucket_name, newdoc_name, copy_doc_name)
        except Exception as e:
            print(f"Error downloading file: {e}")
            return

        if not os.path.isfile(copy_doc_name):
            raise ValueError(f"File {copy_doc_name} was not downloaded correctly")
