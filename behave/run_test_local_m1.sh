export DOCKER_BUILDKIT=1

docker-compose down
docker-compose -f docker-compose.yml -f docker-compose.local.yml -f docker-compose.m1.yml run start_applications
docker-compose exec clabackend bin/create_db.sh
docker-compose up --build cla-end-to-end