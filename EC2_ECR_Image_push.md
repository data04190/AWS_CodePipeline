# EC2_ECR_Image_push

<br>

- git clone
```shell
$ git clone https://github.com/data04190/AWS_CodePipeline.git
```
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

<Br><hr>

Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running? 에러 발생시

```shell
sudo systemctl start docker  #시스템데몬(system daemon) 명령어로 docker를 시작
sudo systemctl status docker   #도커의 상태를 확인  
```
<br>
  
- Docker image 삭제
```shell
$ docker rmi [IMAGE ID] -f   #특정 Image 삭제
$ docker rmi $(docker images -a -q) -f  #Docker images 전부 삭제
```








