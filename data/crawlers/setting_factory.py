import io
import boto3
import pandas as pd
from os import environ
from typing import Type
from dotenv import load_dotenv
from crawlers.platform_setting.base_setting import BaseSetting

load_dotenv(verbose=True)

class Setting():
    def __init__(self, platform_setting: Type[BaseSetting] = None):
        self.AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
        self.AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')
        self.AWS_S3_BUCKET = environ.get('AWS_S3_BUCKET')
        self.AWS_S3_FILE_NAME = environ.get('AWS_S3_FILE_NAME')

        self.BOTO3_SESSION = boto3.Session(
            aws_access_key_id=self.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
        )
        self.S3 = self.BOTO3_SESSION.resource('s3')
        self.platform_name = platform_setting().platform_name if platform_setting else None
        self.platform_url = platform_setting().platform_url if platform_setting else None
        self.query = platform_setting().query if platform_setting else None
        self.referer_list = platform_setting().referer_list if platform_setting else None

    def get_csv_from_s3(self):
        file = self.S3.Object(self.AWS_S3_BUCKET, self.AWS_S3_FILE_NAME).get()['Body'].read()
        df = pd.read_csv(io.BytesIO(file), keep_default_na=False)
        return df