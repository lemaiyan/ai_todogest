"""
Django settings for configurations project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from celery.schedules import crontab
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ks1%$bk%c($-kv=3yamhu9&@ex(*2f*y8$%&b6qhj#5@++jmw6"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'apps.ui',
    'django_celery_beat',
    "apps.oauth",
    "apps.integrations",
    "apps.todo",
    "tinymce",
    "django.contrib.admin",
    "django.contrib.messages",
    "django_google_sso",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.humanize",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "configurations.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.context_processors.baseurl"
            ],
        },
    },
]

WSGI_APPLICATION = "configurations.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT'],
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Nairobi"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(PROJECT_DIR, 'static'))
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.abspath(os.path.join(PROJECT_DIR, 'media'))

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

GOOGLE_SSO_CLIENT_ID = os.environ.get('GOOGLE_SSO_CLIENT_ID')
GOOGLE_SSO_PROJECT_ID = os.environ.get('GOOGLE_SSO_PROJECT_ID', 'todigest')
GOOGLE_SSO_CLIENT_SECRET = os.environ.get('GOOGLE_SSO_CLIENT_SECRET')
GOOGLE_SSO_ALLOWABLE_DOMAINS = ["localhost", "gmail.com"]

# List of emails that will be created as superuser
GOOGLE_SSO_SUPERUSER_LIST = ["jijolemaiyan@gmail.com"]
GOOGLE_REDIRECT_URIS = [
  'http://localhost/google/calendar/redirect/'
]

# If True, the first user that logs in will be created as superuser
# if no superuser exists in the database at all
GOOGLE_SSO_AUTO_CREATE_FIRST_SUPERUSER = True
GOOGLE_SSO_SCOPES = [  # Google default scope
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]
GOOGLE_OAUTH_SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/calendar.readonly", 
                       "https://www.googleapis.com/auth/calendar",
                       'https://www.googleapis.com/auth/gmail.readonly', 
                       'https://www.googleapis.com/auth/gmail.send', 
                       'https://www.googleapis.com/auth/gmail.modify'
                       ]
GOOGLE_SSO_PRE_LOGIN_CALLBACK = "apps.ui.hooks.pre_login_user"
#GOOGLE_SSO_NEXT_URL = "apps.ui:dashboard"
## Chat GPT
CHAGPT_MODEL = "gpt-3.5-turbo"
CHAGPT_KEY = os.environ.get('CHAT_GPT_KEY')

# Celery
CELERY_BROKER_URL = 'amqp://guest:guest@{}:5672/'.format(os.environ.get('RABBITMQ_HOST', 'rabbitmq'))
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
## Email
EMAIL_IMAP_URL = "imap.gmail.com"
EMAIL_HOST_PASSWORD = "tbbx gqno pmqb vonk"
EMAIL_USER = "jijoonfb@gmail.com"
EMAIL_HOST_USER = "jijoonfb@gmail.com"

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}


OUTLOOK_SCOPES = ['Calendars.ReadWrite', 'Mail.ReadWrite', 'Mail.Send', 'User.Read', 'offline_access']
OUTLOOK_CLIENT_ID = os.environ.get('OUTLOOK_CLIENT_ID')
OUTLOOK_CLIENT_SECRET = os.environ.get('OUTLOOK_CLIENT_SECRET')



