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
      postgresql-dev \
      gcc \
      musl-dev \
      postgresql-client \
      python3-dev && \
      pip3 install -U \
      setuptools==59.6.0 \
      pip==21.3.1 \
      wheel==0.37.1

COPY requirements/requirements*.txt requirements/
RUN pip3 install --no-cache-dir -r requirements/requirements-git.txt \
 && pip3 install --no-cache-dir -r requirements/requirements.txt

RUN mkdir /behave
WORKDIR /behave

COPY . .

ENV run_a11y $a11y

ENTRYPOINT ./wrapper.sh $run_a11y