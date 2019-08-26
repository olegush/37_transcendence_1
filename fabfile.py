import os

from environs import Env
from fabric import Connection
from fabric import task
import fabric


env = Env()
env.read_env()

PG_USR = env('PG_USR')
PG_PWD = env('PG_PWD')
PG_DB = env('PG_DB')
SITE = env('SITE')
DIR_SOURCES = env('DIR_SOURCES')
DIR_PROJECT = env('DIR_PROJECT')
DIR_PACKAGE = env('DIR_PACKAGE')
GITHUB_REPO = env('GITHUB_REPO')
GITHUB_NAME = env('GITHUB_NAME')
GITHUB_EMAIL = env('GITHUB_EMAIL')
ENV_DIR = env('ENV_DIR')


def user_exists(c, user):
    result = c.run(f'sudo -i -u postgres psql -t -A -c "SELECT COUNT(*) FROM pg_user WHERE usename=\'{user}\';"')
    return result.stdout.strip() == '1'


def db_exists(c, db):
    result = c.run(f'sudo -i -u postgres psql -t -A -c "SELECT datname FROM pg_catalog.pg_database WHERE datname = \'{db}\';"')
    return result.stdout.strip() == db


@task()
def bootstrap(c):
    # Install packages.
    c.run('apt-get update')
    c.run('apt install python3-pip python3-dev python3-psycopg2 libpq-dev postgresql-10 postgresql-contrib nginx curl')

    # Create postgres DB.
    if not db_exists(c, PG_DB):
        c.run(f'sudo -i -u postgres createdb "{PG_DB}"')
        print(f'{PG_DB} created')

    # Create postgres user.
    if not user_exists(c, PG_USR):
        c.run(f'sudo -i -u postgres psql -t -A -c "CREATE USER ""{PG_USR}"" WITH PASSWORD ""{PG_PWD}"";"')
        print(f'{PG_USR} created')

    # Grant privileges to user.
    c.run(f'sudo -i -u postgres psql -t -A -c "GRANT ALL PRIVILEGES ON DATABASE ""{PG_DB}"" to ""{PG_USR}"";"')

    # Install virtualenv.
    c.run('pip3 install --upgrade pip')
    c.run('pip3 install Pillow')
    c.run('pip3 install virtualenv')

    # Clone repository from GitHub.
    c.run(f'mkdir -p "{DIR_SOURCES}"')
    c.run(f'chown -R www-data:www-data "{DIR_SOURCES}"')
    c.run(f'[ -d "{DIR_SOURCES}"/"{DIR_PROJECT}" ] || git clone "{GITHUB_REPO}" "{DIR_SOURCES}"')

    c.put('.env', DIR_SOURCES)

    with c.cd(DIR_SOURCES):
        c.run(f'[ -d "{ENV_DIR}" ] || virtualenv "{ENV_DIR}"')
        c.run(f'source "{ENV_DIR}"/bin/activate && python3 -m pip install -r requirements.txt')

        # Set Gunicorn configs
        c.run('envsubst < conf_templates/gunicorn.socket.template > /etc/systemd/system/gunicorn.socket')
        c.run(f'export DIR_SOURCES={DIR_SOURCES} && export DIR_PROJECT="{DIR_PROJECT}" && export DIR_PACKAGE="{DIR_PACKAGE}" && export ENV_DIR="{ENV_DIR}" && envsubst < conf_templates/gunicorn.service.template > /etc/systemd/system/gunicorn.service')
        c.run('systemctl start gunicorn.socket')
        c.run('systemctl enable gunicorn.socket')
        c.run('systemctl status gunicorn.socket')
        c.run('systemctl status gunicorn')
        c.run('systemctl daemon-reload')
        c.run('systemctl restart gunicorn')

        # Set Nginx configs
        c.run(f'export DIR_SOURCES="{DIR_SOURCES}" && export DIR_PROJECT="{DIR_PROJECT}" && export SITE="{SITE}" && export KEY=\'$request_uri\' && envsubst < conf_templates/nginx.conf.template > /etc/nginx/sites-available/{DIR_PROJECT}.conf')
        c.run(f'ln -sf /etc/nginx/sites-available/{DIR_PROJECT}.conf /etc/nginx/sites-enabled')
        c.run('ufw delete allow 8000')
        c.run('ufw allow "Nginx Full"')
        c.run('systemctl restart nginx')


@task()
def deploy(c):
    with c.cd(DIR_SOURCES):
        c.run(f'source "{ENV_DIR}"/bin/activate')

        # Git pull
        c.run(f'git config --global user.email "{GITHUB_EMAIL}"')
        c.run(f'git config --global user.name "{GITHUB_NAME}"')
        c.run('git pull')

        # Run Django management commands.
        c.run(f'python3 {DIR_PROJECT}/manage.py migrate')
        c.run(f'python3 {DIR_PROJECT}/manage.py collectstatic')

        c.run('systemctl daemon-reload')
        c.run('systemctl restart gunicorn')
        c.run('systemctl restart nginx')
