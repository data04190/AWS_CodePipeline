#AWS lambda base image
FROM amazon/aws-lambda-python:3.8

#ensure that pip in up to data
RUN /var/lang/bin/python3.8 -m pip install --upgrade pip

# install git 
RUN yum install git -y

# git clone
RUN git clone https://github.com/data04190/AWS_lambda_container.git

# install packages
RUN pip install -r AWS_lambda_container/requirements.txt

# git repository 의 lambda_function.py 를 Container 내부의 /var/task/ 로 이동
RUN cp AWS_lambda_container/lambda_function.py /var/task/

# lambda_function.handler 실행
CMD ["lambda_function.lambda_handler"]
