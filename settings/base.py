import os
from .config import *
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

#SECRET_KEY = os.getenv('SECRET_KEY')
SECRET_KEY = SECRET_KEY

CRISPY_TEMPLATE_PACK = 'bootstrap3'
# Application definition

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'eventsdisplay_app',
    'eventsmanager_app',
    'crispy_forms',
    'django_mysql',
    'storages',
    's3direct',
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

ROOT_URLCONF = 'marverProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['eventsdisplay_app/templates','eventsmanager_app/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media'
            ],
        },
    },
]

WSGI_APPLICATION = 'marverProject.wsgi.application'





# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'eventsmanager_app.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'eventsmanager_app.backends.EmailAuth'
)

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'min_length' : 8,
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-GB'

DATE_INPUT_FORMATS = ('%d-%m-%Y','%Y-%m-%d')

TIME_ZONE = 'GMT'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# https://docs.djangoproject.com/en/1.11/howto/static-files/
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')


STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, '../static'),
)
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880
AWS_STORAGE_BUCKET_NAME = 'elasticbeanstalk-eu-west-2-932524864295'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'eventsmanager_app.custom_storage.MediaStorage'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
AWS_AUTO_CREATE_BUCKET = False
AWS_QUERYSTRING_AUTH = False
AWS_S3_CALLING_FORMAT = 'boto.s3.connection.OrdinaryCallingFormat'
S3DIRECT_REGION = 'eu-west-2'
S3DIRECT_DESTINATIONS = {
    'example_destination': {
        'key': 'media/webcast_videos',
    }
}
