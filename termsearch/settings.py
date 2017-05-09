"""
Django settings for ttsea project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# import local settings containing secretkey and database authentication parameters
try:
    from termsearch.local_settings import *
except ImportError:
    pass

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'aggregator.apps.AggregatorConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'termsearch.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [
            os.path.join(BASE_DIR, '/jinja2/'),
            BASE_DIR
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'termsearch.jinja2.environment',
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]

WSGI_APPLICATION = 'termsearch.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
# imported from local_settings.py

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

# ckeditor WYSIWYG stuff
MEDIA_URL = '/media/'
CKEDITOR_UPLOAD_PATH= 'uploads/'

# Logging settings
# Overwrite the default settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'development_logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django_dev.log'),
            'filters': ['require_debug_true'],
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 50,
            'formatter': 'verbose',

        },
        'production_logfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filters': ['require_debug_false'],
            'filename': os.path.join(BASE_DIR,'logs/django_production.log'),
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 50,
            'formatter': 'simple',

        },
        'dba_logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR,'logs/django_dba.log'),
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 50,
            'formatter': 'verbose',

        },
        'security_logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filters': ['require_debug_false'],
            'filename': os.path.join(BASE_DIR, 'logs/django_security.log'),
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 50,
            'formatter': 'verbose',

        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'aggregator': {
            'handlers': ['console', 'development_logfile', 'production_logfile'],
            'level': 'DEBUG',
        },
        'dba': {
            'handlers': ['console', 'dba_logfile'],
        },
        'django': {
            'handlers': ['console', 'development_logfile', 'production_logfile'],
        },
        'django.security': {
            'handlers': ['console', 'security_logfile'],
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['console', 'development_logfile'],
        },
    }
}

# logging configuration using dictConfig as per Django documentation
