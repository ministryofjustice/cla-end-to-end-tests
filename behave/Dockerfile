FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
      bash \
      tzdata \
      gettext \
      build-essential \
      curl \
      git \
      libxml2-dev \
      libxslt-dev \
      libpq-dev \
      gcc \
      postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install -U setuptools==82.0.1 pip wheel

COPY requirements/requirements*.txt requirements/
RUN pip3 install --no-cache-dir -r requirements/requirements-git.txt \
 && pip3 install --no-cache-dir -r requirements/requirements.txt

RUN mkdir /behave
WORKDIR /behave

COPY . .

ENV run_a11y $a11y

ENTRYPOINT ./wrapper.sh $run_a11y