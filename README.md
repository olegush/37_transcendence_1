# TP project

Blog network prototype based on [Django](https://docs.djangoproject.com/) class based views. Realized: custom user model with "friends" features, extendable blog system with "bookmarks" features.


# How to Install

1. Python 3.6 and libraries from **requirements.txt** should be installed. Use virtual environment tool, for example **virtualenv**.

```bash

virtualenv env
source env/bin/activate
python3 -m pip install -r requirements.txt
```

2. Put vulnerable parameters to **.env** file.

```bash
DEBUG=False
SECRET_KEY=your_django_secret_key
STATIC_URL=STATIC_URL
STATIC_ROOT=STATIC_ROOT
MEDIA_URL=MEDIA_URL
MEDIA_ROOT=MEDIA_ROOT
SITE=127.0.0.1
PG_USR=postgresql_user
PG_PWD=postgresql_password
PG_DB=postgresql_database
DIR_PACKAGE=django_package_directory
EMAIL_HOST=smtp_server_for_emails
EMAIL_HOST_USER=email_from
EMAIL_PORT=smtp_port
EMAIL_HOST_PASSWORD=password
```

3. Run Django
```bash
python3 manage.py runserver
```
and check it on http://127.0.0.1:8000/
