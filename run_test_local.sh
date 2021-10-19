export DOCKER_BUILDKIT=0

docker-compose -f docker-compose.yml -f docker-compose.local.yml run start_applications

docker-compose up cla-end-to-end