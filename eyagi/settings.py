# -*- coding: utf-8 -*-

from __future__ import unicode_literals

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import PASSWORD_HASHERS, LOGIN_REDIRECT_URL,\
    EMAIL_BACKEND, STATICFILES_FINDERS, STATICFILES_DIRS, STATIC_ROOT

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8g#r^g2lipl98=j9j=*-(nm@9j7kdqm*p37%a=#m_f)6mx*doq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
PASSWORD_HASHERS=(
                  'django.contrib.auth.hashers.PBKDF2PasswordHasher',
                  'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
                  'django.contrib.auth.hashers.BCryptPasswordHasher',
                  'django.contrib.auth.hashers.SHA1PasswordHasher',
                  'django.contrib.auth.hashers.MD5PasswordHasher',
                  'django.contrib.auth.hashers.CryptPasswordHasher',
                  )
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'eyagi',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'django.middleware.security.SecurityMiddleware',

)

ROOT_URLCONF = 'eyagi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'eyagi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR+'/staticfiles/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
print STATIC_ROOT
STATICFILES_FINDERS=(
                     'django.contrib.staticfiles.finders.FileSystemFinder',
                     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
                     
                     )
#login
LOGIN_REDIRECT_URL='/'

#email setting
EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'sendgrid_username'
EMAIL_HOST_PASSWORD = 'sendgrid_password'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


#database
#오프라인작업할때 아래 코드를 주석처리해둘것

import dj_database_url

DATABASES['default'] = dj_database_url.config()


