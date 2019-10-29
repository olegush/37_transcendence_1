import os

from environs import Env

env = Env()
env.read_env()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{env("PROJECT_NAME")}.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')

from configurations.wsgi import get_wsgi_application

application = get_wsgi_application()
