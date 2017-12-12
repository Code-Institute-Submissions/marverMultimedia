from .base import *
import os

DEBUG = False

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'marver',
            'USER': os.getenv('DATABASE_USERNAME'),
            'PASSWORD':os.getenv('DATABASE_PASSWORD'),
            'HOST':os.getenv('DATABASE_HOST'),
            'PORT' : os.getenv('DATABASE_PORT'),
            'OPTIONS':{
                'charset' : 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    }
        }
}

SITE_URL = 'https://marverproject.herokuapp.com'
ALLOWED_HOSTS.append('marverproject.herokuapp.com')
ALLOWED_HOSTS.append('localhost')

STRIPE_PUBLISHABLE = os.getenv('STRIPE_PUBLISHABLE')
STRIPE_SECRET =  os.getenv('STRIPE_SECRET')

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
    },
}

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880
AWS_STORAGE_BUCKET_NAME = 'elasticbeanstalk-eu-west-2-932524864295'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_S3_HOST = 's3.eu-west-2.amazonaws.com'
STATIC_HOST = '/https://elasticbeanstalk-eu-west-2-932524864295.s3.amazonaws.com' if not DEBUG else ''
STATIC_URL = "/https://%s/" % AWS_S3_CUSTOM_DOMAIN
