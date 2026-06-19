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
      postgresql-client && \
      pip3 install -U \
      setuptools \
      pip \
      wheel

COPY requirements/requirements*.txt requirements/
RUN pip3 install --no-cache-dir -r requirements/requirements-git.txt \
 && pip3 install --no-cache-dir -r requirements/requirements.txt

RUN mkdir /behave
WORKDIR /behave

COPY . .

ENV run_a11y $a11y

ENTRYPOINT ./wrapper.sh $run_a11y