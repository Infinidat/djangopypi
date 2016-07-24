"""
Django settings for djangopypi project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(__file__)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class':'logging.StreamHandler'
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True
        },
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True
        }
    }
}


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dje5tfuo1xah%8ld%10vl)521(p5lna&fd3wf1k*t1e0imz=83'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'registration',
    'app',
    'djangopypi',
    'haystack'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'app.urls'

WSGI_APPLICATION = 'app.wsgi.application'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '../../collected_static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

import os
DATABASE_FILEPATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 os.pardir,
                                                 os.pardir,
                                                 'devdatabase.db'))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASE_FILEPATH,
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = False
USE_TZ = False

DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i:s'


DJANGOPYPI_ALLOW_VERSION_OVERWRITE = False
DJANGOPYPI_RELEASE_UPLOAD_TO = 'dists'
DJANGOPYPI_PROXY_MISSING = True # proxy missing [simple] packages to pypi.python.org/simple
DEFAULT_FILE_STORAGE = 'djangopypi.views.distutils.FileSystemStorage_PEP440'
MEDIA_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 os.pardir,
                                                 os.pardir,
                                                 'media'))
MEDIA_URL = '/media/'

REGISTRATION_OPEN = True
ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_REDIRECT_URL = "/"

HAYSTACK_CONNECTIONS = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(BASE_DIR, 'haystack')

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'haystack')
    }
}
