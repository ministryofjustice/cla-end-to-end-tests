DUMP_FILE="./data/cla_backend.$(git rev-parse --abbrev-ref HEAD).backup.sql"
echo "DUMP FILE IS :$DUMP_FILE"
docker-compose exec db pg_dump cla_backend -U postgres -f $DUMP_FILE
# Remove this SET statement otherwise import of the db will fail
sed -i '' '/SET default_table_access_method = heap;/d' $DUMP_FILE

if test -f "./data/cla_backend.main.backup.sql"; then
  echo "RESTORING PREVIOUS DATABASE"
  docker-compose exec prev_db psql cla_backend -U postgres -a -f "./data/cla_backend.main.backup.sql"
fi
docker-compose run --entrypoint "python3 /behave_local/helper/yapgdd/main.py" cla-end-to-end
