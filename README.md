# Simple OTA (Over the Air)

## What is it

This is a simple solution for any OTA workflow that you can have in your IoT project.
There are a few components that are used in this workflow.

- An S3 bucket to store the files.
- Dynamodb table to store the metadata of the files.
- A serverless api to create new revisions of the files. (Admin upload)
- A serverless api to get the latest version of the file. (To be used by device to download)

The project contains a bin directory with the upload script.

## How to use it

### Prerequisites

- aws account (resources used fit in free tier)
- aws cli
- serverless installed

### Setup
Copy `.env.example` and fill in with your data. 
Run `sls deploy`

Once the API is ready, fill in the remaining env variables. Then use `./upload.sh` to upload files.

### Usage from device

Use any HTTP library to fetch the file metadata. 
The response will contain the latest firmware to fetch from AWS along with a timestamp signifying the upload date.
You can check to see if the device needs an update and if so, download the file and begin firmware update.

### Removing service

Run `sls remove`

## License
Copyright Bartłomiej Lewandowski

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
