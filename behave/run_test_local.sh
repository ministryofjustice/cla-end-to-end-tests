#!/bin/bash
export DOCKER_BUILDKIT=0

while [ -n "$1" ]; do # while loop starts
	case "$1" in
	--database-snapshot-enabled)

	  echo "Running with database snapshot enabled"
	  export DATABASE_SNAPSHOT_ENABLED=True
	;; # Message for -a option
	esac
	shift
done

docker-compose down
docker-compose -f docker-compose.yml run start_applications
docker-compose exec clabackend bin/create_db.sh
docker-compose up --build cla-end-to-end
