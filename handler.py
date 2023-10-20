import json
import os

import boto3
from botocore.exceptions import ClientError
import logging
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
TABLE_NAME=os.environ['DYNAMODB_TABLE']


def get_current_date_iso_str():
    current_date = datetime.now()
    return current_date.isoformat()


class FirmwareVersions:
    def __init__(self):
        self.table = dynamodb.Table(TABLE_NAME)

    def get_object_by_key(self, key):
        try:
            response = self.table.get_item(Key={"key": key})
        except ClientError as err:
            logging.error(
                "Couldn't table item with key %s from table %s. Here's why: %s: %s",
                key,
                self.table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return response["Item"]

    def add_object(self, key, s3_url):
        try:
            response = self.table.update_item(
                Key={"key": key},
                UpdateExpression="set s3Url=:s3Url, lastUpdated=:lastUpdated",
                ExpressionAttributeValues={
                    ":s3Url": s3_url,
                    ":lastUpdated": get_current_date_iso_str(),
                },
            )
        except ClientError as err:
            logging.error(
                "Couldn't update table item with key %s from table %s. Here's why: %s: %s",
                key,
                self.table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return response


table = FirmwareVersions()


def handle(event, _):
    method = event['requestContext']['http']['method']
    if method == 'GET':
        if 'key' not in event['pathParameters']:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Missing key parameter"})
            }
        result = table.get_object_by_key(event['pathParameters']['key'])
        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }
    elif method == 'POST':
        if 'x-upload-secret' not in event['headers']:
            return {
                "statusCode": 403,
                "body": "Missing x-upload-secret header"
            }
        if event['headers']['x-upload-secret'] != os.environ['UPLOAD_SECRET']:
            return {
                "statusCode": 403,
                "body": json.dumps({"m": "Invalid x-upload-secret header", "r": event})
            }
        parsed = json.loads(event['body'])

        if 'key' not in parsed or 's3Url' not in parsed:
            return {
                "statusCode": 400,
                "body": "Missing key or s3Url in body"
            }
        result = table.add_object(parsed['key'], parsed['s3Url'])
        return {
            "statusCode": 204
        }
    return {
        "statusCode": 400,
        "body": 'Invalid method.'
    }
