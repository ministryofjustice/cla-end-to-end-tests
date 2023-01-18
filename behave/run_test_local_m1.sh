#!/bin/bash
export DOCKER_BUILDKIT=0
a11y=${1:-"not_set"}
if [ $a11y = "not_set" ]; then
  export A11Y_SET="false"
else
  export A11Y_SET="true"
fi

echo "a11y environment $A11Y_SET"

docker-compose down
docker-compose -f docker-compose.yml -f docker-compose.local.yml -f docker-compose.m1.yml up -d clafrontend

# Use docker image, do not build for cla-public
docker-compose -f docker-compose.yml -f docker-compose.m1.yml up -d clapublic
docker-compose -f docker-compose.yml -f docker-compose.local.yml -f docker-compose.m1.yml up -d clabackend
docker-compose -f docker-compose.yml -f docker-compose.local.yml -f docker-compose.m1.yml up -d seleniumchrome
docker-compose exec clabackend bin/create_db.sh
docker-compose build cla-end-to-end --build-arg a11y=$A11Y_SET
docker-compose up -d cla-end-to-end