FROM python:3.8-slim-bookworm AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
      curl \
      git \
      libxml2-dev \
      libxslt-dev \
      libpq-dev \
      gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install -U setuptools==70.0.0 pip wheel

COPY requirements/requirements*.txt requirements/
RUN pip3 install --no-cache-dir -r requirements/requirements-git.txt \
 && pip3 install --no-cache-dir -r requirements/requirements.txt


FROM python:3.8-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
      bash \
      tzdata \
      gettext \
      libpq5 \
      postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

RUN mkdir /behave
WORKDIR /behave

COPY . .

ENV run_a11y $a11y

ENTRYPOINT ./wrapper.sh $run_a11y
