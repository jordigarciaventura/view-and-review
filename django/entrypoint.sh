#!/bin/bash

ENV_PATH=.env

# Load environment variables
if [[ -f  $ENV_PATH ]] ; then
  echo "Loading environment variables..."
else
  echo "File $ENV_PATH not found, aborting."
  exit 1
fi

while read -r LINE; do
  if [[ $LINE == *'='* ]] && [[ $LINE != '#'* ]]; then
    ENV_VAR="$(echo $LINE | envsubst)"
    eval "declare $ENV_VAR"
  fi
done < $ENV_PATH

# Apply database migrations
if [ "$DJANGO_MIGRATE_DB_ON_STARTUP" != "False" ]; then
  echo "Running database migrations..."
  python manage.py migrate --noinput
fi

# Create django admin superuser
python manage.py createsuperuser --noinput

exec "$@"
