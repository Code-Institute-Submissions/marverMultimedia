from .base import *

DEBUG = False

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'eb',
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

SITE_URL = 'https://marverproject.herokuapp.com'
ALLOWED_HOSTS.append('marverproject.herokuapp.com')

STRIPE_PUBLISHABLE = os.getenv('STRIPE_PUBLISHABLE',STRIPE_PUBLISHABLE)
STRIPE_SECRET =  os.getenv('STRIPE_SECRET',STRIPE_SECRET)

AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY

EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD

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