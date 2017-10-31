import os
from .config import *
from .base import *
DEBUG = True

ALLOWED_HOSTS.append('localhost')

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'marver',
            'USER': DATABASE_USERNAME,
            'PASSWORD':DATABASE_PASSWORD,
            'HOST':DATABASE_HOST,
            'PORT' : DATABASE_PORT,
            'OPTIONS':{
                'charset' : 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    }
        }
}

STRIPE_PUBLISHABLE = os.getenv('STRIPE_PUBLISHABLE',STRIPE_PUBLISHABLE)
STRIPE_SECRET =  os.getenv('STRIPE_SECRET',STRIPE_SECRET)

AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY

EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
#STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'