"""
Django settings for youtubeService project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

WEBSITE_NAME = "local-youtube-service"
# the name for the directory that the settings.py file is in
PROJECT_MAIN_APP_NAME="youtubeService"
# AUTH_USER_MODEL = "authentication.User"

WEBSITE_GLOBAL_URL = f'{WEBSITE_NAME}.herokuapp.com'

# it can be "cmd" or "file"
logging_type =  os.getenv("LOGGING_TYPE")

# global or local
database_status = os.getenv("DATABASE_STATUS")
# global or local
server_status = os.getenv("SERVER_STATUS")

# convert string to boolean
USE_S3 = (os.getenv("USE_S3") == "True")
USE_AWS_FOR_OFFLINE_USAGE = (os.getenv("USE_AWS_FOR_OFFLINE_USAGE") == "True")
DEBUG = (os.getenv("DEBUG") == "True")


LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv("SECRET_KEY")


if server_status == "local":
    ALLOWED_HOSTS = ["127.0.0.1", "0.0.0.0"]
    if database_status == "local":
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.getenv("POSTGRES_DB"),
                'USER': os.getenv("POSTGRES_USER"),
                'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
                'HOST': os.getenv("POSTGRES_HOST"),
                'PORT': os.getenv("POSTGRES_PORT"),
            }
        }
    elif database_status == "global":
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.getenv("GLOBAL_POSTGRES_DB"),
                'USER': os.getenv("GLOBAL_POSTGRES_USER"),
                'PASSWORD': os.getenv("GLOBAL_POSTGRES_PASSWORD"),
                'HOST': os.getenv("GLOBAL_POSTGRES_HOST"),
                'PORT': os.getenv("GLOBAL_POSTGRES_PORT"),
            }
        }

    else:
        raise ValueError("database_status is not recognized.(try to use global or  local ")

elif server_status == "global":
    ALLOWED_HOSTS = ['*']
    if database_status == "global":
        DATABASES={}
        DATABASES['default'] = dj_database_url.config()
    else:
        raise("The website can't run a dev(local) database on a global server")

else:
    raise ValueError("server_status is not recognized.(try to use global or  local ")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'storages',

    "page404.apps.Page404Config",
    "logAuthentication.apps.LogauthenticationConfig",
    "main.apps.MainConfig",
    "mail.apps.MailConfig",

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

]

ROOT_URLCONF = f'{PROJECT_MAIN_APP_NAME}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = f'{PROJECT_MAIN_APP_NAME}.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



if logging_type is "file":
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                'datefmt' : "%d/%b/%Y %H:%M:%S"
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': 'mysite.log',
                'formatter': 'verbose'
            },
        },
        'loggers': {
            'django': {
                'handlers':['file'],
                'propagate': True,
                'level':'DEBUG',
            },
            'MYAPP': {
                'handlers': ['file'],
                'level': 'DEBUG',
            },
        }
    }
elif logging_type is "cmd":
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'NOTSET',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'NOTSET',
            },
            'django.request': {
                'handlers': ['console'],
                'propagate': False,
                'level': 'ERROR'
            }
        }
    }
else:
    pass


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files (CSS, JavaScript, Images)
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#
# # Extra places for collectstatic to find static files.
# STATICFILES_DIRS = (
#     os.path.join(STATIC_ROOT, 'static'),
# )
#
# MEDIA_ROOT = os.path.join(STATIC_ROOT, "media")

# EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
#
#
# SENDGRID_API_KEY = config.get('email', 'SENDGRID_API_KEY')
# DEFAULT_FROM_EMAIL = config.get('email', 'DEFAULT_FROM_EMAIL')

# aws s3 settings
if USE_S3:
    # aws settings
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    # s3 static settings
    AWS_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
else:

    if USE_AWS_FOR_OFFLINE_USAGE:

        AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
        AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
        AWS_DEFAULT_ACL = 'public-read'
        AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
        AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
        # s3 static settings
        STATIC_LOCATION = 'static'
        STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
        STATICFILES_STORAGE = f'{PROJECT_MAIN_APP_NAME}.storage_backends.StaticStorage'
        # s3 public media settings
        PUBLIC_MEDIA_LOCATION = 'media'
        MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
        DEFAULT_FILE_STORAGE = f'{PROJECT_MAIN_APP_NAME}.storage_backends.PublicMediaStorage'
        # s3 private media settings
        PRIVATE_MEDIA_LOCATION = 'private'
        PRIVATE_FILE_STORAGE = f'{PROJECT_MAIN_APP_NAME}.storage_backends.PrivateMediaStorage'
    else:
        STATIC_URL = '/static/'
        STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
        MEDIA_URL = '/mediafiles/'
        MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'staticfiles'),)


# CELERY_BROKER_URL = 'redis://localhost:6379'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379'
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = TIME_ZONE
