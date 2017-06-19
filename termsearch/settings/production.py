"""
Production settings for live server

$ workon myenv
$ vi $VIRTUAL_ENV/bin/postactivate
#!/bin/bash
# This hook is run after this virtualenv is activated.
export DJANGO_SETTINGS_MODULE = 'termsearch.settings.production'
export SECRET_KEY='mysupersecretkey'
export DBNAME = 'yourdbname'
export DBUSER = 'yourdbuser'
export DBPASSWORD = 'yourdbpassword'
export DBHOST = 'mydbhost'

save and quit
check that it worked

$ deactivate
$ workon myenv
$ echo $DJANGO_SETTINGS_MODULE
termsearch.settings.production

Add the hooks to cleanup the env variables when the virtual environment is removed

vi $VIRTUAL_ENV/bin/predeactivate
unset DJANGO_SETTINGS_MODULE
unset SECRET_KEY
unset DBNAME
unset DBUSER
unset DBPASSWORD
unset DBHOST

save and quit


"""

from .base import *

ALLOWED_HOSTS += ['termsearch.me', 'www.termsearch.me', '207.154.244.48']

DEBUG = False

SECRET_KEY = get_env_variable('SECRET_KEY')

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