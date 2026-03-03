FROM cimg/python:3.14.3

RUN pip install awscli docker-compose==1.27.4
COPY behave .