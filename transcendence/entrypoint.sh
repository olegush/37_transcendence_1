#!/bin/sh

if [ "$PG_DB" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $PG_HOST $PG_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py migrate
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('superuser@superuser.com', 'pwd12345')" | python manage.py shell
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_user('user@user.com', 'pwd123')" | python manage.py shell

exec "$@"
