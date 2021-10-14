# cla-end-to-end-tests
This is the behave end to end tests which cover the CLA applications for the laa-cla-fala team.

## Current state of affairs
The commands to get this running locally are:

Note: to build this locally you need to set:

`export DOCKER_BUILDKIT=0`

to build locally:
`docker-compose -f docker-compose.yml -f docker-compose.local.yml up -d --build`

then run the container:
`docker-compose up cla-end-to-end`

another way is to bash into the container and run them from there:
`docker-compose run --entrypoint /bin/bash cla-end-to-end`