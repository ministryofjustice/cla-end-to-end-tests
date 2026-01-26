# 🧪 CLA End-to-End Tests

[![Ministry of Justice Repository Compliance Badge](https://github-community.service.justice.gov.uk/repository-standards/api/cla-end-to-end-tests/badge)](https://github-community.service.justice.gov.uk/repository-standards/cla-end-to-end-tests)

## 📋 Overview

This is the Behave end-to-end test suite which covers the CLA applications for the laa-cla-fala team.
This repository defines a CircleCI orb and a Docker image alongside the `behave` test suite itself,
allowing portability to the CI pipelines of the other applications.

## ⚙️ CircleCI Orb

The orb is defined as a single `orb.yml` file and is currently published manually to a dev tag.
Once we have credentials from the Operations Engineering team, we will be able to publish production
releases of the orb, which we will do from CircleCI.

### 📦 Publishing the Orb

To publish the dev orb, you need to have the `CircleCI CLI` installed and set up, and to be a member
of the `ministryofjustice` organisation, which you should be from GitHub.

```bash
circleci orb publish orb.yml ministryofjustice/cla-end-to-end-tests@dev:first
```

To incorporate orb publishing into the CI pipeline in the future, we may want to use the `circleci/orb-tools` orb.

### 🔧 Job and Command

The orb exposes a `behave` job and a `behave` command. The command should not need to be used directly:
the job simply runs this command on a suitable executor (using the Docker image built from this repository).

### 💡 Example Usage

The `config.yml` of an application using the orb may look something like this:

```yaml
version: 2.1
orbs:
  cla-end-to-end-tests: ministryofjustice/cla-end-to-end-tests@dev:first

workflows:
  version: 2
  build_and_test:
    jobs:
      - test
      - build:
          requires:
            - test
      - cla-end-to-end-tests/behave:
          requires:
            - build
          pre-steps:
            - checkout:
                path: cla_backend
            - run:
                command: |
                  cd cla_backend
                  source .circleci/define_build_environment_variables testing
                  echo "export CLA_BACKEND_IMAGE=$ECR_DEPLOY_IMAGE" >> $BASH_ENV
                  echo "Setting CLA Backend image $ECR_DEPLOY_IMAGE"
```

In this example, a command is run in the `pre-steps` stage in order to set an environment variable in the `$BASH_ENV`,
allowing the pipeline to specify that the test suite uses the newly-built application image rather than
the default.

## 🐳 Docker Image

This repository builds a Docker image that is then used as the executor for the `behave` CircleCI job.
You are unlikely to need to use the image directly elsewhere.
