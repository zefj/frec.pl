"""
Extension settings file example for development and/or production. This is a straight copy of the production settings file I use on the server, obviously excluding sensitive data.
 
"""

"""
Production settings.

"""

from base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Static and media files (CSS, JavaScript, Images)
# Media lies outside of the project folder, hence this peculiar MEDIA_ROOT

MEDIA_URL ='/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
