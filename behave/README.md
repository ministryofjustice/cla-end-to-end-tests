# cla-end-to-end-tests
This is the behave end to end tests which cover the CLA applications for the laa-cla-fala team.

This readme assumes that the working directory is that of this document, which is no longer the
root of this repository: the root of this repository now provides a means to deliver and use the
functionality in this directory.

## Current state of affairs Intel users
The commands to get this running locally are:

To run the tests locally just run this script:

`./run_test_local.sh`

If you want a more manual approach:

`export DOCKER_BUILDKIT=0`

to build locally:
`docker-compose -f docker-compose.yml -f docker-compose.local.yml up -d --build`

bash into the container and run them from there:
`docker-compose run --entrypoint /bin/bash cla-end-to-end`

## Current state of affairs Apple Silicon (arm64) users

Apples new line of computers (Apple Silicon) no longer use Intel processors. Instead, Apple has made their own, (at the time of writing) it isn't widely supported. 

Before running command below, make sure you are logged into your AWS via the aws command-line tool. 
Please see [Authenticating to your docker image repository](https://user-guide.cloud-platform.service.justice.gov.uk/documentation/deploying-an-app/helloworld-app-deploy.html#authenticating-to-your-docker-image-repository)

To run the tests locally just run this script for Apple Silicon users. 

`./run_test_local_m1.sh`

**What are the known problems for Apple Silicon users?**

Currently, `phantom.js` is used for unit testing in cla_frontend and does not support `arm64` which causes `uwsgi` to fail to start.

`events.js` within `cla_public`, throws an unhandled error 'qemu-i386', this is because '/lib/ld-linux.so.2' directory does not exist in `arm64` platforms.

Selenium Chrome also does not support `arm64`. In order to get it to work use this docker image: `seleniarm/standalone-chromium:4.0.0-beta-1-20210215`
[seleniarm](https://github.com/SeleniumHQ/docker-selenium#experimental-mult-arch-aarch64armhfamd64-images)

Within `behave/docker-compose.m1.yml`, changes have been made to allow `cla_frontend` and `cla_public` to build correctly. If the required platform architecture values. e.g. `platform: linux/arm64` are not set, the build fails.
This is because both `cla_frontend` and `cla_public` have dependencies that fail unless the platform architecture is specified.

**Side notes**

`cla_backend` does not require a platform architecture value change, as `cla_backend` builds and runs successfully on an `arm64` machine.

## Using your local Chrome browser [optional]
If you want to see the tests running in your hosts machines Chrome browser and still have the applications 
running in their containers then do the following.
You need to make sure that you have a version of chromedriver that matches your version of chrome.
```
brew install chromedriver
python3 -m pip install -r requirements.txt
chromedriver # take note of the port listed. Will stay running in the foreground
```

### Running the tests
```
# Run all the tests
./run_test_local_chrome_driver.sh

# Run tests with the "createuser" tag
./run_test_local_chrome_driver.sh -t "createuser"
```

## Lint and pre-commit hooks

To lint with Black and flake8, install pre-commit hooks:
```
virtualenv -p python3 env --prompt=\(cla_e2e\)
. env/bin/activate
pip install -r requirements.txt
pre-commit install
```

To run them manually:
```
pre-commit run --all-files
```