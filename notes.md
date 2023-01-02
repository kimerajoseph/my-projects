## build image
docker build -t scada-kinesis-events:v1 .

### Publishing Docker images

Creating an ECR repo

```bash
aws ecr create-repository --repository-name duration-model
```

Logging in
# this is what worked for login. pipe the output of get password to docker
aws ecr get-login-password | docker login --username AWS --password-stdin <aws-account-no>.dkr.ecr.eu-west-3.amazonaws.com

Pushing 

```bash
REMOTE_URI="<aws-account-no>.dkr.ecr.eu-west-3.amazonaws.com/power-system"
REMOTE_TAG="v3"
REMOTE_IMAGE=${REMOTE_URI}:${REMOTE_TAG}
LOCAL_IMAGE="scada-kinesis-events:v3"
docker tag ${LOCAL_IMAGE} ${REMOTE_IMAGE}
docker push ${REMOTE_IMAGE}
```


aws kinesis register-stream-consumer --stream-arn <your-stream-arn> --consumer-name <your-lambda-function-name>

aws kinesis register-stream-consumer --stream-arn arn:aws:kinesis:eu-west-3:<aws-account-no>:stream/power-system-stream --consumer-name scada-process-events


## ERROR ENCOUNTERED
1. empty dataframe resulting in merger when substations are not in list
2. index column on DB tables created with sqlaclhemy
3. s3 path to save file (needs to be a file eg s3://<bucket-name>/filename.parquet)

