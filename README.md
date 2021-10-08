# cla-end-to-end-tests
This is the behave end to end tests which cover the CLA applications for the laa-cla-fala team.

## Current state of affairs
This now works within two docker containers locally.

The end to end tests use the Dockerfile for running the tests, and a standalone-chrome docker container done by selenium here [selenium-docker](https://github.com/SeleniumHQ/docker-selenium)

The commands to get this running locally are:

`docker-compose -f docker-compose.yml -f docker-compose.local.yml up -d --build`

`docker-compose up cla-end-to-end`

`docker-compose run --entrypoint /bin/bash cla-end-to-end`