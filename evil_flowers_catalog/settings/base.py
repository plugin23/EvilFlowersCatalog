"""
Django settings for updater_api project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import datetime
import json
import os
from datetime import timedelta
from pathlib import Path
from urllib.parse import urlparse

import sentry_sdk
from dotenv import load_dotenv
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
ENV_FILE = os.path.join(BASE_DIR, '.env')
LOG_DIR = os.path.join(BASE_DIR, 'logs')
BUILD_FILE = Path(f"{BASE_DIR}/BUILD.txt")
VERSION_FILE = Path(f"{BASE_DIR}/VERSION.txt")

# .env
if os.path.exists(ENV_FILE):
    load_dotenv(dotenv_path=ENV_FILE, verbose=True)

BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1:8000')
BASE_DOMAIN = urlparse(BASE_URL).netloc
INSTANCE_NAME = os.getenv('INSTANCE_NAME', 'Evil Flowers Catalog')

if BUILD_FILE.exists():
    with open(BUILD_FILE) as f:
        BUILD = f.readline().replace('\n', '')
else:
    BUILD = datetime.datetime.now().isoformat()

if VERSION_FILE.exists():
    with open(VERSION_FILE) as f:
        VERSION = f.readline().replace('\n', '')
else:
    VERSION = 'dev'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.postgres',

    'corsheaders',
    'django_api_forms',

    'apps.core',
    'apps.api',
    'apps.files'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'apps.api.middleware.exceptions.ExceptionMiddleware',
]

ROOT_URLCONF = 'evil_flowers_catalog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.opds.context_processors.basic_settings'
            ],
        },
    },
]

WSGI_APPLICATION = 'evil_flowers_catalog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT', 5432),
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', None)
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

AUTH_USER_MODEL = "core.User"

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

OBJECT_CHECKERS_MODULE = 'apps.core.checkers'

SECURED_VIEW_AUTHENTICATION_SCHEMAS = {
    'Basic': 'apps.core.auth.BasicBackend',
    'Bearer': 'apps.core.auth.BearerBackend'
}

SECURED_VIEW_JWT_ALGORITHM = 'RS256'
SECURED_VIEW_JWK = json.loads(os.getenv('SECURED_VIEW_JWK'))
SECURED_VIEW_JWT_ACCESS_TOKEN_EXPIRATION = timedelta(
    minutes=int(os.getenv('SECURED_VIEW_JWT_ACCESS_TOKEN_EXPIRATION', 5))
)
SECURED_VIEW_JWT_REFRESH_TOKEN_EXPIRATION = timedelta(
    minutes=int(os.getenv('SECURED_VIEW_JWT_REFRESH_TOKEN_EXPIRATION', 60 * 24))
)

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

DATETIME_INPUT_FORMATS = ('%Y-%m-%dT%H:%M:%S%z',)

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 100  # 100MB

# Sentry
if os.getenv('SENTRY_DSN', False):
    def before_send(event, hint):
        if 'exc_info' in hint:
            exc_type, exc_value, tb = hint['exc_info']
            if exc_type.__name__ in ['ValidationException']:
                return None
        if 'extra' in event and not event['extra'].get('to_sentry', True):
            return None

        return event

    sentry_sdk.init(
        integrations=[DjangoIntegration()],
        attach_stacktrace=True,
        send_default_pii=True,
        request_bodies='always',
        before_send=before_send,
    )

# Redis
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
REDIS_DATABASE = int(os.getenv('REDIS_DATABASE', '0'))

# Pagination
PAGINATION = {
    'DEFAULT_LIMIT': 10
}

OPDS = {
    'NEW_LIMIT': 20,
    'IMAGE_UPLOAD_MAX_SIZE': 1024 * 1024 * 5,  # 5MB
    'IMAGE_MIME': (
        'image/gif',
        'image/jpeg',
        'image/png',
    ),
    'IMAGE_THUMBNAIL': (768, 480),
    'CRON_JOBS': {
        'popularity': '*/5 * * * *'
    },
    'IDENTIFIERS': [
        'isbn', 'google'
    ]
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

CORS_ALLOW_ALL_ORIGINS = True

# Storage
STORAGE_DRIVER = os.getenv('STORAGE_DRIVER', 'apps.files.storage.filesystem.FileSystemStorage')

# Filesystem storage
STORAGE_FILESYSTEM_DATADIR = os.getenv('STORAGE_FILESYSTEM_DATADIR')

# S3 Storage
STORAGE_S3_HOST = os.getenv('STORAGE_S3_HOST')
STORAGE_S3_ACCESS_KEY = os.getenv('STORAGE_S3_ACCESS_KEY')
STORAGE_S3_SECRET_KEY = os.getenv('STORAGE_S3_SECRET_KEY')
STORAGE_S3_SECURE = False
STORAGE_S3_BUCKET = os.getenv('STORAGE_S3_BUCKET')
