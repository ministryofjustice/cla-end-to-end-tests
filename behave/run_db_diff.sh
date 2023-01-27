CLEANED_BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD | sed 's/^feature[-/]//' | sed 's:^\w*\/::' | tr -s ' _/[]().' '-' | tr '[:upper:]' '[:lower:]' | cut -c1-28 | sed 's/-$//')
DUMP_FILE="/data/cla_backend.$CLEANED_BRANCH_NAME.backup"
echo "DUMP FILE IS :$DUMP_FILE"
#docker-compose exec db pg_dump cla_backend --username postgres --file $DUMP_FILE
docker-compose exec db pg_dump cla_backend --clean --blobs --format=custom --host=db --username=postgres --file=$DUMP_FILE

if test -f "./data/cla_backend.main.backup"; then
  echo "RESTORING PREVIOUS DATABASE"
   docker-compose exec prev_db pg_restore --clean --dbname=cla_backend /data/cla_backend.main.backup
fi
docker-compose run --entrypoint "python3 /behave_local/helper/yapgdd/main.py" cla-end-to-end
