# 🧪 CLA End-to-End Tests

[![Ministry of Justice Repository Compliance Badge](https://github-community.service.justice.gov.uk/repository-standards/api/cla-end-to-end-tests/badge)](https://github-community.service.justice.gov.uk/repository-standards/cla-end-to-end-tests)

## 📋 Overview

This is the Behave end-to-end test suite which covers the CLA applications for the Changes to Client Access to Legal Advice (CALA) team.
This repository defines a GitHub Action reusable workflow `e2e.yml` alongside the `behave` test suite itself,
allowing portability to the CI pipelines of other applications.

## ⚙️ GHA Reusable workflow

Using GitHub Actions, we have the reusable workflow `e2e.yml` which it can be used across any of our services.
To do so, you add this step in your pipeline `uses: ministryofjustice/cla-end-to-end-tests/.github/workflows/e2e.yml@main`

### 🔧 What it does

The workflow pulls the latest images of the repos that are being tested (cla_frontend, cla_frontend_socketserver, cla_backend),
and runs the tests defined in this repo. 

### 💡 Example Usage

The `e2e.yml` of an application using the workflow may look something like this:

```yaml
  end-to-end-tests:
    needs: [build-and-push]
    permissions:
      contents: read
      id-token: write
    uses: ministryofjustice/cla-end-to-end-tests/.github/workflows/e2e.yml@main
    with:
      CLA_FRONTEND_IMAGE: "${{ vars.CLA_FRONTEND_ECR_REPOSITORY }}:${{ needs.build-and-push.outputs.image_tag }}"
      CLA_FRONTEND_ECR_REGION: ${{ vars.CLA_FRONTEND_ECR_REGION}}
      CLA_BACKEND_ECR_REGION: ${{ vars.CLA_BACKEND_ECR_REGION}}
      SOCKET_SERVER_ECR_REGION: ${{ vars.SOCKET_SERVER_ECR_REGION }}
    secrets:
      CLA_FRONTEND_ECR_ROLE_TO_ASSUME: ${{ secrets.CLA_FRONTEND_ECR_ROLE_TO_ASSUME }}
      CLA_BACKEND_ECR_ROLE_TO_ASSUME: ${{ secrets.CLA_BACKEND_ECR_ROLE_TO_ASSUME }}
      SOCKET_SERVER_ECR_ROLE_TO_ASSUME: ${{ secrets.SOCKET_SERVER_ECR_ROLE_TO_ASSUME }}
      ECR_REGISTRY_URL: ${{ secrets.ECR_REGISTRY_URL }}
```

In this example from cla_frontend, you can see the action requires the [build-and-push] action first in order to set 
an environment variable in the `CLA_FRONTEND_IMAGE`, allowing the pipeline to specify that the test suite uses the newly-built
application image rather than the default.


