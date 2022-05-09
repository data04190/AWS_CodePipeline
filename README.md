# AWS_lambda_container

<br>

- AWS CLI 설치

```shell
$ curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
$ unzip awscliv2.zip
$ sudo ./aws/install
```
<br>

- Image Build
```shell
$ docker build -t [이미지명] .
```
<br>

- ECR 환경설정
```shell
$ export ACCOUNT_ID=$(aws sts get-caller-identity --output text --query Account)
$ echo "export ACCOUNT_ID=${ACCOUNT_ID}" | tee -a ~/.bash_profile
```
<br>

- Image tagging
```shell
$ docker tag "[이미지명]" $ACCOUNT_ID.dkr.ecr."ap-northeast-2".amazonaws.com/"[리포지토리명]"
```
<br>

- ECR Image 업로드
```shell
$ aws ecr get-login-password --region "ap-northeast-2" | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr."ap-northeast-2".amazonaws.com
$ docker push $ACCOUNT_ID.dkr.ecr."ap-northeast-2".amazonaws.com/"[리포지토리명]"
```





