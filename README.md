# cla-end-to-end-tests
This is the behave end to end test suite which covers the CLA applications for the laa-cla-fala team.
This repository defines a Circlei CI orb and a docker image alongside the `behave` test suite itself,
allowing portability to the CI pipelines of the other applications.


## CircleCI Orb
The orb is defined as a single `orb.yml` file and is currently published manually and to a dev tag.
Once we have credentials from the Operations Engineering team, we will be able to publish production
releases of the orb, which we will do from Circle CI.

### Job and command
The orb exposes a `behave` job and a `behave` command. The command should not need to be used directly:
the job simply runs this command on a suitable executor (using the docker image built from this repo).

### Example usage
The `config.yml` of an application using the orb may look something like this:
```
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
In this example, a command is run in the `pre-steps` stage in order to set an env var in the `$BASH_ENV`,
allowing the pipeline to specify that the test suite uses the newly-built application image rather than
the default.

## Docker image
This repository builds a docker image that is then used as the executor for the `behave` Circle CI job.
You are unlikely to need to use the image directly elsewhere.
