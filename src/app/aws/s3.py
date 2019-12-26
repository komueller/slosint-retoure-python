import os

import boto3

from app.infrastructure import constants


def get_file(filename: str):
    s3 = _get_s3()

    try:
        result = s3.get_object(Bucket=os.environ[constants.AWS_S3_BUCKET_ENV_NAME], Key=filename)
        return result['Body'].read()
    except Exception as e:
        print(f"A S3 error occurred: {repr(e)}")
        raise e


def _get_s3():
    return boto3.client("s3", constants.AWS_REGION)
