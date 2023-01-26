export DOCKER_BUILDKIT=0

docker-compose down
docker-compose -f docker-compose.yml -f docker-compose.local.yml -f docker-compose.m1.yml up -d clafrontend
export DOCKER_BUILDKIT=1
# Use docker image, do not build for cla-public
docker-compose -f docker-compose.yml -f docker-compose.m1.yml up -d clapublic
docker-compose -f docker-compose.yml -f docker-compose.local.yml -f docker-compose.m1.yml up -d clabackend
docker-compose -f docker-compose.yml -f docker-compose.local.yml -f docker-compose.m1.yml up -d seleniumchrome
docker-compose exec clabackend bin/create_db.sh
docker-compose up --build cla-end-to-end