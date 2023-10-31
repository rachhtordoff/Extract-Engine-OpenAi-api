# aws_service.py
import boto3
from botocore.client import Config as aws_config
from src.config import Config as conf 

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
        copy_doc_name = f'/opt/src/documents/{doc_name}'
        
        self.client.download_file(bucket_name, newdoc_name, copy_doc_name)
