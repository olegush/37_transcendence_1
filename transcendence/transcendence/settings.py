import os
from typing import Dict, List, Tuple, Union

from environs import Env
from configurations import Configuration

env = Env()
env.read_env()


class Dev(Configuration):

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = env('SECRET_KEY')


    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG =  env.bool('DEBUG')


    ALLOWED_HOSTS = [f'{env("SITE")}']


    # Application definition

    INSTALLED_APPS = [
        'channels',
        'users',
        'posts',
        'chat',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]

    WSGI_APPLICATION = f'{env("DIR_PACKAGE")}.wsgi.application'

    ASGI_APPLICATION = 'routing.application'

    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                "hosts": [('127.0.0.1', 6379)],
            },
        },
    }

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = f'{env("DIR_PACKAGE")}.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                    os.path.normpath(os.path.join(BASE_DIR, 'templates')),
                ],
            'OPTIONS': {
                "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
                ],
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]



    # Database
    # https://docs.djangoproject.com/en/2.2/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env('PG_DB'),
            'USER': env('PG_USR'),
            'PASSWORD': env('PG_PWD'),
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }


    # Password validation
    # https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]
    #I&$#GVT#^zfd

    AUTH_USER_MODEL = 'users.CustomUser'

    LOGIN_REDIRECT_URL = '/my_posts'
    LOGOUT_REDIRECT_URL = '/'


    # Internationalization
    # https://docs.djangoproject.com/en/2.2/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'Europe/Moscow'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.2/howto/static-files/
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]
    MEDIA_URL = env('MEDIA_URL')
    MEDIA_ROOT = os.path.join(BASE_DIR, env('MEDIA_ROOT'))

    # Security
    # https://docs.djangoproject.com/en/2.2/topics/security/

    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True

    X_FRAME_OPTIONS = 'DENY'

    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy#Syntax
    REFERRER_POLICY = 'no-referrer'

    # https://github.com/adamchainz/django-feature-policy#setting
    FEATURE_POLICY: Dict[str, Union[str, List[str]]] = {}  # noqa: TAE002


    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = 'tmp/emails'
    #EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    #EMAIL_HOST = env('EMAIL_HOST')
    #EMAIL_PORT = env('EMAIL_PORT')
    #EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    #EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
    #EMAIL_USE_TLS = True
