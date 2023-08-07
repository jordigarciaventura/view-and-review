#!/bin/bash

# Load environment variables
if [[ -f x.txt ]] ; then
  echo "Loading environment variables..."
else
  echo 'File ".env" is not there, aborting.'
  exit 1
fi

while read -r LINE; do
  if [[ $LINE == *'='* ]] && [[ $LINE != '#'* ]]; then
    ENV_VAR="$(echo $LINE | envsubst)"
    eval "declare $ENV_VAR"
  fi
done < .env

# Apply database migrations
if [ "$DJANGO_MIGRATE_DB_ON_STARTUP" != "False" ]; then
  echo "Running database migrations..."
  python manage.py migrate --noinput
fi

# Create django admin superuser
python manage.py createsuperuser --noinput

exec "$@"
