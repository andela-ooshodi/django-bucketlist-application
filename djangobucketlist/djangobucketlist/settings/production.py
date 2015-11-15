# Production specific settings
from .base import *
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': dj_database_url.config()
}

BOWER_PATH = '/app/node_modules/bower'

# Enable Persistent Connections
DATABASES['default']['CONN_MAX_AGE'] = 500

# Enable Connection Pooling
DATABASES['default']['ENGINE'] = 'django_postgrespool'
