#!/usr/bin/env bash

KEY=$1
FILENAME=$2

if [ -z "$BUCKET_NAME" ]; then
    echo "Please run source .env first."
    exit 1
fi

if [ -z "$UPLOAD_SECRET" ]; then
    echo "Please run source .env first."
    exit 1
fi

#check if 2 arguments are passed
if [ $# -ne 2 ]; then
    echo "Usage: ./upload.sh <key> <filename>"
    exit 1
fi

if [ ! -f "$FILENAME" ]; then
  echo "File $FILENAME does not exist"
  exit 1
fi

date=$(date '+%Y-%m-%d-%H-%M-%S')
UPLOAD_FILENAME="firmware_${date}"

echo "Uploading $FILENAME to S3 as $UPLOAD_FILENAME"
aws s3 cp $FILENAME s3://$BUCKET_NAME/$UPLOAD_FILENAME

UPLOADED_FILE_S3_URL="http://$BUCKET_NAME.s3.amazonaws.com/$UPLOAD_FILENAME"
PAYLOAD="{\"key\":\"$KEY\",\"s3Url\":\"$UPLOADED_FILE_S3_URL\"}"

echo "Sending payload: $PAYLOAD" to $API_URL
curl -X POST $API_URL \
   -H 'Content-Type: application/json' \
   -H "x-upload-secret: $UPLOAD_SECRET" \
   -d "{\"key\":\"$KEY\",\"s3Url\":\"$UPLOADED_FILE_S3_URL\"}"
