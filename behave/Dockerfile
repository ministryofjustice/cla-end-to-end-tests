FROM docker.io/alpine:3.23.3@sha256:25109184c71bdad752c8312a8623239686a9a2071e8825f20acb8f2198c3f659

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
      postgresql-dev \
      gcc \
      musl-dev \
      postgresql-client \
      python3-dev && \
    pip3 install -U setuptools pip wheel

COPY requirements.txt requirements.txt
RUN pip3 install -r ./requirements.txt

RUN mkdir /behave
WORKDIR /behave

COPY . .

ENV run_a11y $a11y

ENTRYPOINT ./wrapper.sh $run_a11y