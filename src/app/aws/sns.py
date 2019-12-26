import os

import boto3

from app.infrastructure import constants


def publish(retoure_xml: str):
    if len(retoure_xml) == 0:
        raise Exception("The retoure xml is empty")

    try:
        sns = _get_sns()
        sns.publish(
            os.environ[constants.AWS_SNS_TOPIC_ARN_ENV_NAME], Message=retoure_xml
        )
    except Exception as e:
        print(f"A SNS error occurred: {repr(e)}")
        raise e


def _get_sns():
    return boto3.client("sns", constants.AWS_REGION)
