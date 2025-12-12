# cla-end-to-end-tests
This is the behave end-to-end test suite which covers the CLA applications for the laa-cla-fala team.
This repository defines a Circlei CI orb and a docker image alongside the `behave` test suite itself,
allowing portability to the CI pipelines of the other applications.


## CircleCI Orb
The orb is defined as a single `orb.yml` file and is currently published manually and to a dev tag.
Once we have credentials from the Operations Engineering team, we will be able to publish production
releases of the orb, which we will do from Circle CI.

### Publishing the orb
To publish the dev orb, you need to have the `CircleCI CLI` installed and set up, and to be a member
of the `ministryofjustice` organisation, which you should be from github.
```
circleci orb publish orb.yml ministryofjustice/cla-end-to-end-tests@dev:first
```
To incorporate orb publishing into the CI pipeline in the future, we may want to use the `circleci/orb-tools` orb

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

3. **Activation**

   Execute the following command in the repository directory

   ```bash
   prek install
   ```

4. **Test**

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
