FROM python:3.13-alpine AS builder

RUN apk add --no-cache \
  build-base \
  curl \
  git \
  libxml2-dev \
  libxslt-dev \
  postgresql-dev

RUN pip3 install -U setuptools==70.0.0 pip wheel

COPY requirements/requirements*.txt requirements/
RUN pip3 install --no-cache-dir -r requirements/requirements-git.txt \
 && pip3 install --no-cache-dir -r requirements/requirements.txt


FROM python:3.13-alpine

RUN apk add --no-cache \
      libpq \
      libxml2 \
      libxslt

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

RUN mkdir /behave
WORKDIR /behave

COPY . .

ENTRYPOINT ["./wrapper.sh"]
