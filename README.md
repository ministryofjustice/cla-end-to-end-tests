# cla-end-to-end-tests
This is the behave end to end tests which cover the CLA applications for the laa-cla-fala team.

## Current state of affairs
The commands to get this running locally are:

To run the tests locally just run this script:

`./run_test_local.sh`

If you want a more manual approach:

`export DOCKER_BUILDKIT=0`

to build locally:
`docker-compose -f docker-compose.yml -f docker-compose.local.yml up -d --build`

bash into the container and run them from there:
`docker-compose run --entrypoint /bin/bash cla-end-to-end`

## Using your local chrome browser [optional]
If you want to see the tests running in your hosts machines chrome browser and still have the applications 
running in their containers then do the following.
```
brew install chromedriver
pip install -r requirements.txt
chromedriver # take note of the port listed. Will stay running in the foreground
```

If it does not exist create a `.env` file in the root of the project and add the following
```
CLA_E2E_BACKEND_URL=http://localhost:8010
CLA_E2E_FRONTEND_URL=http://localhost:8011
CLA_E2E_SELENIUM_WEB_DRIVER_URL=http://localhost:9515
```
Finally run the tests in your host running `behave` in your host terminal