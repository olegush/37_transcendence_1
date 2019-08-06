# Transcendence project

[TODO. There will be project description]


# How to Install

1. Python 3.6 and libraries from **requirements.txt** should be installed. Use virtual environment tool, for example **virtualenv**.

```bash

virtualenv virtualenv_folder_name
source virtualenv_folder_name/bin/activate
python3 -m pip install -r requirements.txt
```

2. For errors logging register account on [sentry.io](https://sentry.io/), connect with Django and get your SENTRY DSN KEY.

3. Put vulnerable parameters to **.env** file.

```bash
DEBUG=False
SECRET_KEY=your_django_secret_key
SENTRY_DSN=your_sentry_dsn_key
```

4. Run Django
```bash
python3 manage.py runserver
```

5. Check it on http://127.0.0.1:8000/


# How to deploy

1. Get server with Ubuntu LTS, for example on [digitalocean.com](https://cloud.digitalocean.com/)

2. Add vulnerable parameters to **.env** file.

```bash
SITE=your_domain_or_ip
PG_USR=postgresql_user
PG_PWD=postgresql_password
PG_DB=postgresql_database
DIR_SOURCES=directory_with_your_sources
DIR_PROJECT=django_project_directory
DIR_PACKAGE=django_package_directory
GITHUB_REPO=your_repository_url_on_github
GITHUB_NAME=your_username_on_github
GITHUB_EMAIL=your_email_on_github
ENV_DIR=directory_with_your_remote_virtual_environment
```

3. Run **fabfile.py** with arguments:
```bash
fab --hosts=root@your_domain_or_ip deploy
```

4. Check out your site on http://your_domain_or_ip

5. Make some changes in template, for example, push to GitHub, run **fabfile.py** again and check it.

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
