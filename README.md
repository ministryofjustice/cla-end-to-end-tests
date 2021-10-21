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