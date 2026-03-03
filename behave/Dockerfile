# Base
FROM docker.io/alpine:3.23.3@sha256:25109184c71bdad752c8312a8623239686a9a2071e8825f20acb8f2198c3f659

# Dependencies
RUN apk add --no-cache \
      bash \
      py3-pip \
      tzdata \
      gettext

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
      python3-dev

# Environment
ENV PYTHON_VIRTUAL_ENV=/venv
RUN python3 -m venv $PYTHON_VIRTUAL_ENV
ENV PATH="$PYTHON_VIRTUAL_ENV/bin:$PATH"

# Install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r ./requirements.txt

# Execute
RUN mkdir /behave
WORKDIR /behave

COPY . .

ENV run_a11y=$a11y
ENTRYPOINT ./wrapper.sh $run_a11y
