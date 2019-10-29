import os
import sys

from environs import Env

env = Env()
env.read_env()


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{env("PROJECT_NAME")}.settings')
    os.environ.setdefault('DJANGO_CONFIGURATION', f'{env("CONFIGURATION")}')

    try:
        from configurations.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
