# cla-end-to-end-tests
This is the behave end to end tests which cover the CLA applications for the laa-cla-fala team.

## Current state of affairs
This now works within two docker containers locally.

The end to end tests use the Dockerfile for running the tests, and a standalone-chrome docker container done by selenium here [selenium-docker](https://github.com/SeleniumHQ/docker-selenium)

Build the docker container first:
`docker build . -t behave/cla`

To run the tests in an interactive bash container use this command:

`docker run -it --entrypoint /bin/bash --network host --rm -v "$(pwd):/behave:ro" behave/cla`

In another terminal run this for the chromedriver/browser:

`docker run -d --network host --shm-size="2g" selenium/standalone-chrome:4.0.0-rc-2-prerelease-20210908`

Note they are running in the same network of host so that they can talk to each other.

Back in the terminal with bash running you can just run the below command to run the tests.

`behave`

All updates in test files will be automatically reflected in the container.