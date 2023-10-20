### Prerequisites

- aws cli
- logged into aws cli

### Usage

Run ./upload.sh with following parameters
- key to use for the file (stg, prd etc...)
- filename to upload

```bash
source .env
./upload.sh stg ./test.txt
```

### What it does

- Uploads the file to S3, gets the url to download
- Calls a serverless api method to add this file as the newest version for the given key
