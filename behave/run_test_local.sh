#!/bin/bash
# Exit immediately if there is an error
set -e

export DOCKER_BUILDKIT=0

function start_applications {
  docker-compose -f docker-compose.yml run start_applications
}

function run_migrations {
  docker-compose exec clabackend bin/create_db.sh
}

function run_tests {
  docker-compose up --build cla-end-to-end
}


while [ -n "$1" ]; do # while loop starts
	case "$1" in
	--diff-with-branch)
	  export DATABASE_SNAPSHOT_ENABLED=True
	  shift
	  echo "Doing database diff"
	  export DIFF_IMAGE=$1
	  echo "Comparing master backend with $DIFF_IMAGE"
	  docker pull $DIFF_IMAGE
	;;
	--a11y)
	  echo "Running with A11Y enabled"
    export A11Y_ENABLED=True
	esac
	shift
done

docker-compose down
start_applications
run_migrations
run_tests

if [ "$DIFF_IMAGE" != "" ]; then
    # Take snapshot of the current database
    docker-compose exec db pg_dump cla_backend \
      --clean \
      --blobs \
      --format=custom \
      --host=db \
      --username=postgres \
      --file=/data/cla_backend.main.backup
    # disable exiting on error temporarily
    set +e
    # Restore snapshot to second database service
    docker-compose exec prev_db pg_restore --clean --dbname=cla_backend /data/cla_backend.main.backup
    set -e

    # reset the database and backend
    docker-compose rm -fsv db clabackend
    export CLA_BACKEND_IMAGE=$DIFF_IMAGE
    start_applications

    # rerun the tests
    run_migrations
    run_tests

    # Do the database diff
    docker-compose run --entrypoint "python3 /behave_local/helper/yapgdd/main.py" cla-end-to-end
fi

