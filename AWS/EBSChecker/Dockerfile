FROM python:3.9-slim-buster

RUN pip3 install --upgrade boto3==1.16.8 botocore==1.19.8

COPY ebs_checker.py /opt/ebs_checker.py

ENTRYPOINT ["python3", "/opt/ebs_checker.py"]
CMD ["--help"]