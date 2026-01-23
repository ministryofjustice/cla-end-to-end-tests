FROM python:3.10-alpine

RUN apk add --no-cache \
      bash \
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
      postgresql-dev \
      gcc \
      musl-dev \
      postgresql-client


RUN python -m pip install --upgrade pip setuptools wheel

COPY requirements.txt requirements.txt
RUN python -m pip install -r ./requirements.txt

RUN mkdir /behave
WORKDIR /behave

COPY . .

ENV run_a11y $a11y

ENTRYPOINT ./wrapper.sh $run_a11y