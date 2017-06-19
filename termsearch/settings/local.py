from .base import *

ALLOWED_HOSTS += ['127.0.0.1', 'localhost']

MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware'
]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# for django debug toolbar
INTERNAL_IPS = ['127.0.0.1']

SECRET_KEY = get_env_variable('TERMSEARCH_LOCAL_SECRET_KEY')


INSTALLED_APPS += [
    'debug_toolbar',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env_variable('DBNAME'),
        'USER': get_env_variable('DBUSER'),
        'PASSWORD': get_env_variable('DBPASSWORD'),
        'HOST': get_env_variable('DBHOST'),
        'PORT': '',
    }
}
