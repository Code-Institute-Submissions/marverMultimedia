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

STRIPE_PUBLISHABLE = os.getenv('STRIPE_PUBLISHABLE','pk_test_hLMNTIjTI5BX4SLzE7buyXz4')
STRIPE_SECRET =  os.getenv('STRIPE_SECRET','sk_test_4BdY6pB0aw6qgpvGYpriWfbu')

AWS_ACCESS_KEY_ID = 'AKIAIRFEXJBPBFK3RDRQ'
AWS_SECRET_ACCESS_KEY = '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'

EMAIL_HOST_USER = 'AKIAIYWXMV6YC536YTWA'
EMAIL_HOST_PASSWORD = 'AqjdlIaIwn4xMfD0lKAVw3qzApIM8y141D+QTvJ4WTtM'

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