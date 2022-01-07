FROM cimg/python:3.10.1

RUN pip install awscli docker-compose==1.27.4
COPY behave .