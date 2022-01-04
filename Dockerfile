FROM cimg/python:3.10.1

RUN pip install awscli
COPY behave .