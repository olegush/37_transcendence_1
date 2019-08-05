import os

from environs import Env
from dotenv import load_dotenv
from fabric import Connection
from fabric import task
import fabric


env = Env()
env.read_env()

PG_USR = env('PG_USR')
PG_PWD = env('PG_PWD')
PG_DB = env('PG_DB')
DIR = env('DIR')
GIT_REPO = env('GIT_REPO')
ENV_DIR = env('ENV_DIR')


def user_exists(c, user):
    result = c.run(f'sudo -i -u postgres psql -t -A -c "SELECT COUNT(*) FROM pg_user WHERE usename=\'{user}\';"')
    return result.__dict__['stdout'].strip() == '1'


def db_exists(c, db):
    result = c.run(f'sudo -i -u postgres psql -t -A -c "SELECT datname FROM pg_catalog.pg_database WHERE datname = \'{db}\';"')
    return result.__dict__['stdout'].strip() == db


@task()
def bootstrap(c):
    #c.run('[ -d "transcendence" ] &&  echo "does not exists" fi')

    c.run('apt-get update')
    c.run('apt install python3-pip python3-dev python3-psycopg2 libpq-dev postgresql-10 postgresql-contrib nginx curl')

    if not db_exists(c, PG_DB):
        c.run(f'sudo -i -u postgres createdb {PG_DB}')
        print(f'{PG_DB} created')

    if not user_exists(c, PG_USR):
        c.run(f'sudo -i -u postgres psql -t -A -c "CREATE USER {PG_USR} WITH PASSWORD \'{PG_PWD}\';"')
        print(f'{PG_USR} created')

    c.run(f'sudo -i -u postgres psql -t -A -c "GRANT ALL PRIVILEGES ON DATABASE {PG_DB} to {PG_USR};"')
    c.run('pip3 install --upgrade pip')
    c.run('pip3 install virtualenv')
    c.run(f'mkdir -p {DIR}')


    c.run(f'[ -d {DIR}/{DIR} ] || git clone {GIT_REPO} {DIR}')

    c.put('.env', DIR)

    with c.cd(DIR):
        c.run(f'[ -d {ENV_DIR} ] || virtualenv {ENV_DIR}')
        c.run(f'source {ENV_DIR}/bin/activate && python3 -m pip install -r requirements.txt')
        c.run('git pull')
        c.run(f'python3 {DIR}/manage.py makemigrations')
        c.run(f'python3 {DIR}/manage.py migrate')
        c.run(f'python3 {DIR}/manage.py migrate')
        c.run(f'python3 {DIR}/manage.py collectstatic')












    #c.run('mv /etc/postgresql/10/main/pg_hba.conf /etc/postgresql/10/main/pg_hba.confbak2')
    #c.run('mv /etc/postgresql/10/main/pg_hba.confbak /etc/postgresql/10/main/pg_hba.conf')
    #c.put('pg_hba.conf', '/etc/postgresql/10/main/')
    #c.run('service postgresql restart')


    #c.run('passwd postgres')




    #c.run('whoami')
    #c.run('cd /')
    #

    #else:
    #    print('y')
    #if not user_exists(c, PG_USR):
    #    c.run(f'sudo -i -u postgres psql -t -A -c "CREATE USER {PG_USR} WITH PASSWORD \'pwD31456\';"')







    #c.run('psql -U postgres template1')

    #c.run('psql -U postgres -c "ALTER USER postgres WITH password \'pwd1\';"')

    #c.run('psql -U postgres -W  -h localhost')
    #c.run('psql "CREATE ROLE {0} WITH PASSWORD \'{1}\' NOSUPERUSER CREATEDB NOCREATEROLE LOGIN;"'.format('user', 'pwd'))
    #c.run('psql -U postgres -c "CREATE DATABASE {0} WITH OWNER={1} TEMPLATE=template0 ENCODING=\'utf-8\';"'.format('db', 'user'))


    #c.run('\l')
    #c.run('exit')
