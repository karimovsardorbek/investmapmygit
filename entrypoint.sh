#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Run makemigrations to capture any model changes
python manage.py makemigrations --noinput

# Run migrations to apply any pending migrations
python manage.py migrate --noinput

exec "$@"
