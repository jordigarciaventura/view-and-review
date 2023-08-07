#!/bin/bash

# Apply database migrations
if [ "$DJANGO_MIGRATE_DB_ON_STARTUP" != "false" ]; then
  echo "Running database migrations..."
  python manage.py migrate --noinput
fi

# Create django admin superuser
python manage.py createsuperuser --noinput

exec "$@"
