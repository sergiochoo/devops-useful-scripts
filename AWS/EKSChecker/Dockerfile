FROM python:3.9-slim-buster

RUN pip3 install --upgrade boto3==1.16.8 botocore==1.19.8

COPY eks_checker.py /opt/eks_checker.py

ENTRYPOINT ["python3", "/opt/eks_checker.py"]
CMD ["--help"]