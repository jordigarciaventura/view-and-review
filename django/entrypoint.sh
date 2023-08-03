#!/bin/bash

# Load environment variables from file
source .env

if [ "$DJANGO_MIGRATE_DB_ON_STARTUP" != "False" ]; then
  echo "Running database migrations..."
  python manage.py migrate --noinput
fi

python manage.py createsuperuser --noinput

exec "$@"