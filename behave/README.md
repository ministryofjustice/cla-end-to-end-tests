# cla-end-to-end-tests

This is the behave end to end tests which cover the CLA applications for the laa-cla-fala team.

This readme assumes that the working directory is that of this document, which is no longer the
root of this repository: the root of this repository now provides a means to deliver and use the
functionality in this directory.

## Test file structure

Each feature file is seperated out into their own directory to help make it easier to organise each services test.

## Testing branches in Circleci

When you need to test a targeted branch in CircleCi, you will need to add
`echo "export E2E_BRANCH= >> $BASH_ENV` within your targeted branch projects CircleCi config.
This will need to be applied under your projects CircleCi config `behave` values.

Cla_backend feature files:

`behave > features > cla_backend`

Cla_frontend feature files:

`behave > features > cla_frontend`

## How to run tests

If you are working on an M1 machine, please add the below to your behave/.env file. There is an example file at .env.m1.example that you can rename to .env to avoid doing this.

'ALPINE_BASE_IMAGE='arm64v8/alpine:3.15'
NODE_BASE_IMAGE='amd64/node:10'
SELENIUM_IMAGE='seleniarm/standalone-chromium:latest''

To run all tests, execute in main behave directory (/behave_local if bashed into Docker container):

`behave`

To run selective tests or test tag:

Single
`behave -t @tag1`

Multiple
`behave -t @tag1,@tag2,@tag3`

## Current state of affairs Intel users

The commands to get this running locally are:

To run the tests locally just run this script:

`./run_test_local.sh`

If you want a more manual approach:

`export DOCKER_BUILDKIT=0`

to build locally:
`docker-compose -f docker-compose.yml -f docker-compose.local.yml up -d --build`

bash into the container and run them from there:
`docker-compose run --entrypoint sh cla-end-to-end`

## Current state of affairs Apple Silicon (arm64) users

Apples new line of computers (Apple Silicon) no longer use Intel processors. Instead, Apple has made their own, (at the time of writing) it isn't widely supported.

Before running command below, make sure you are logged into your AWS via the aws command-line tool.
Please see [Authenticating to your docker image repository](https://user-guide.cloud-platform.service.justice.gov.uk/documentation/deploying-an-app/helloworld-app-deploy.html#authenticating-to-your-docker-image-repository)

To run the tests locally just run this script for Apple Silicon users.

`./run_test_local_m1.sh`

**What are the known problems for Apple Silicon users?**

Currently, `phantom.js` is used for unit testing in cla_frontend and does not support `arm64` which causes `uwsgi` to fail to start.

Selenium Chrome also does not support `arm64`. In order to get it to work use this docker image: `seleniarm/standalone-chromium:4.0.0-beta-1-20210215`
[seleniarm](https://github.com/SeleniumHQ/docker-selenium#experimental-mult-arch-aarch64armhfamd64-images)

Within `behave/docker-compose.m1.yml`, changes have been made to allow `cla_frontend` to build correctly. If the required platform architecture values. e.g. `platform: linux/arm64` are not set, the build fails.
This is because `cla_frontend` has dependencies that fail unless the platform architecture is specified.

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

### Run Accessibility tests

[axe-selenium-python](https://pypi.org/project/axe-selenium-python/)
[core-documentation](https://www.deque.com/axe/core-documentation/api-documentation)

To turn on accessibility checks, set the 'define' value.
`behave -D a11y=true`

To call all accessibility tests with `@a11y-check` tags
`behave -D a11y=true -t @a11y-check`

Finding the a11y.json report
`behave/data/a11y_reports/a11y.json`

Reports are generated at the end of a single test or whole run test run.

## Lint and pre-commit hooks

To lint with Black and flake8, install pre-commit hooks:

```
virtualenv -p python3 env --prompt=\(cla_e2e\)
. env/bin/activate
pip3 install -r requirements.txt
pre-commit install
```

To run them manually:

```
pre-commit run --all-files
```

## Database diff

This involves running the end-to-end tests twice, once using images defined in the docker-compose.yml and again using
a given backend image.

For example to run a diff between the resulting database of end-to-end test using backend master and
the image of the django-upgrade branch which is django-upgrade.de199c9

```
./run_test_local.sh --diff-with-branch 754256621582.dkr.ecr.eu-west-2.amazonaws.com/laa-get-access/cla_backend:django-upgrade.de199c9
```

This should output a summary of all the tables that are different across the two databases.
A more detailed difference of each table is created in the data/yapgdd/ folder, one .log file for each table

## Git hooks

Repository uses [MoJ DevSecOps hooks](https://github.com/ministryofjustice/devsecops-hooks) to ensure `pre-commit` git hook is evaluated for series of checks before pushing the changes from staging area. Engineers should ensure `pre-commit` hook is configured and activated.

1. **Installation**:
   Ensure [prek](https://github.com/j178/prek?tab=readme-ov-file#installation) is installed globally
   Linux / MacOS

   ```bash
   curl --proto '=https' --tlsv1.2 -LsSf https://raw.githubusercontent.com/ministryofjustice/devsecops-hooks/e85ca6127808ef407bc1e8ff21efed0bbd32bb1a/prek/prek-installer.sh | sh
   ```

   or

   ```bash
   brew install prek
   ```

   Windows

   ```bash
   powershell -ExecutionPolicy ByPass -c "irm https://raw.githubusercontent.com/ministryofjustice/devsecops-hooks/e85ca6127808ef407bc1e8ff21efed0bbd32bb1a/prek/prek-installer.ps1 | iex"
   ```

2. **Activation**

   Execute the following command in the repository directory

   ```bash
   prek install
   ```

3. **Test**

    To dry-run the hook

   ```bash
   prek run
   ```

## 🔧 Configuration

### Exclusion list

One can exclude files and directories by adding them to `exclude` property. Exclude property accepts [regular expression](https://pre-commit.com/#regular-expressions).

Ignore everything under `reports` and `docs` directories for `baseline` hook as an example.

```yaml
   repos:
     - repo: https://github.com/ministryofjustice/devsecops-hooks
       rev: v1.0.0
       hooks:
         - id: baseline
            exclude: |
            ^reports/|
            ^docs/
```

Or one can also create a file with list of exclusions.

```yaml
repos:
  - repo: https://github.com/ministryofjustice/devsecops-hooks
    rev: v1.0.0
    hooks:
      - id: baseline
        exclude: .pre-commit-ignore
```
