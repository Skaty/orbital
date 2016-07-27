"""
Django settings for projection project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

import bleach
from django.contrib.messages import constants as message_constants
import dj_database_url


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3_v8)xa7+_9-m=1=b5(^+_nslvzmaox3tefx)w1vv3eu!eh%vc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_nose',
    'postman',
    'projects.apps.ProjectsConfig',
    'targets.apps.TargetsConfig',
    'miscellaneous.apps.MiscellaneousConfig',
    'social.apps.django_app.default',
    'profiles.apps.ProfilesConfig',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'projection.middleware.TimezoneMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'projection.backends.NUSOpenId',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'projection.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.dirname(os.path.realpath(__file__)) + "/templates", ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'projection.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

if os.getenv('PROJECTION_APP_ENV', 'debug') == 'production':
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

if os.getenv('PROJECTION_APP_ENV', 'debug') == 'production':
    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Test Runner Configuration
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Redirects

LOGIN_URL = '/auth/login/'

LOGIN_REDIRECT_URL = '/'

# Messaging

MESSAGE_TAGS = {
    message_constants.ERROR: 'danger'
}

# Python Social Auth

SOCIAL_AUTH_URL_NAMESPACE = 'sso'

# Timezones

DEFAULT_TZ = 'Asia/Singapore'

# Bleach

BLEACH_ALLOWED_TAGS = bleach.ALLOWED_TAGS + [
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'img',
    'p',
    'sup',
    'sub',
    'code',
]

EXTRA_ALLOWED = {
    'img': ['src', 'alt', 'width', 'height'],
    'p': ['style'],
}

BLEACH_ALLOWED_ATTRIBUTES = {**bleach.ALLOWED_ATTRIBUTES, **EXTRA_ALLOWED}

# django-postman
POSTMAN_DISALLOW_ANONYMOUS = True
POSTMAN_AUTO_MODERATE_AS = True
POSTMAN_DISABLE_USER_EMAILING = True
POSTMAN_NOTIFIER_APP = None
POSTMAN_MAILER_APP = None

# Django Sites
SITE_ID = 1