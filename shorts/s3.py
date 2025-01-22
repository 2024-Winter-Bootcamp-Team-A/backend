import boto3

import os
from dotenv import load_dotenv 

load_dotenv()

def s3_connection():
    try:
        s3 = boto3.client(
            service_name="s3",
            aws_access_key_id=os.environ.get('S3_ACCESS_KEY'),
            aws_secret_access_key=os.environ.get('S3_SECRET_KEY'),
            region_name="ap-northeast-2",
        )
    except Exception as e:
        print(e)
    else:
        return s3


def upload_file(in_file):
    output_file = in_file
    s3 = s3_connection()
    s3.upload_file(in_file, os.environ.get('S3_BUCKET'), output_file)

    return "https://teama-bookshorts.s3.ap-northeast-2.amazonaws.com/" + output_file