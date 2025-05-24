#!/bin/bash

set -e

echo "Waiting for DB..."
# Проверка подключения к БД
while ! nc -z db 5432; do
  sleep 1
done

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Creating superuser..."
DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-admin}
DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-admin@example.com}
DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-admin}

# Создаем суперпользователя только если его нет
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="${DJANGO_SUPERUSER_USERNAME}").exists():
    User.objects.create_superuser("${DJANGO_SUPERUSER_USERNAME}", "${DJANGO_SUPERUSER_EMAIL}", "${DJANGO_SUPERUSER_PASSWORD}")
    print("Superuser created.")
else:
    print("Superuser already exists.")
END

# Загружаем начальные данные, если они не загружены
echo "Loading initial data (if not loaded)..."
if ! python manage.py showmigrations | grep initial_data; then
    python manage.py loaddata initial_data.json || true
fi

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
exec "$@"
