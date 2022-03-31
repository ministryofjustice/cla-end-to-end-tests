export DOCKER_BUILDKIT=0

docker-compose down
docker-compose -f docker-compose.yml -f docker-compose.local.yml run start_applications
docker-compose exec clabackend bin/create_db.sh
docker-compose exec clabackend python manage.py loaddata test_special_provider_case.json
docker-compose up --build cla-end-to-end