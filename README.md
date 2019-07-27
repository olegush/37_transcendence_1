# Transcendence project

[TODO. There will be project description]


# How to Install

Python 3.6 and libraries from **requirements.txt** should be installed. Use virtual environment tool, for example **virtualenv**.

```bash

virtualenv virtualenv_folder_name
source virtualenv_folder_name/bin/activate
python3 -m pip install -r requirements.txt
```

For errors logging register account on [sentry.io](https://sentry.io/), connect with Django and get your SENTRY DSN KEY.

Put vulnerable parameters to **.env** file.

```bash
DEBUG=False
SECRET_KEY=your_django_secret_key
SENTRY_DSN=your_sentry_dsn_key
```

Run Django
```bash
python3 manage.py runserver
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
