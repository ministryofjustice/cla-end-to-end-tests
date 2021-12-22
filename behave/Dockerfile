FROM alpine:3.9

RUN apk add --no-cache \
      bash \
      py3-pip \
      tzdata \
      gettext

# To install pip dependencies
RUN apk add --no-cache \
      build-base \
      curl \
      git \
      libxml2-dev \
      libxslt-dev \
      linux-headers \
      python3-dev && \
    pip3 install -U setuptools pip==18.1 wheel

COPY requirements.txt requirements.txt
RUN pip3 install -r ./requirements.txt

RUN mkdir /behave
COPY . /behave

COPY ./wrapper.sh wrapper.sh

ENTRYPOINT ["./wrapper.sh"]
