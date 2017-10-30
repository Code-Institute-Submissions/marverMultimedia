import os
from .base import *
from .config import *

DEBUG = True

ALLOWED_HOSTS.append('localhost')

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


