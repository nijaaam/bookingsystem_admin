"""
Django settings for bookingsystem_admin project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AZURE_ACCOUNT_NAME = "dbbackupbksys"
AZURE_ACCOUNT_KEY  = 'CkD5/KNWSF/BV4sM0XcnyrfBgPmZXjQW4i/FR4l2wX2Mn/PMZtZ/5u9D2wP6JUpXHDyJUwDtaiAECnuOYBPmfw=='
AZURE_CONTAINER = 'admindb'

DEFAULT_FILE_STORAGE = 'storage.AzureStorage'
DBBACKUP_STORAGE = DEFAULT_FILE_STORAGE


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=3v%n_g54=o&5p4*l@lm%#*49f@+kx)d&@1a=dbnrc^7)oxmz-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'login.CustomUser'
# Application definition
DATABASE_ROUTERS = ['bksys.router.DBRouter']
INSTALLED_APPS = [
    'login',
    'bksys',
    'storages',
    'dbbackup',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
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

ROOT_URLCONF = 'bookingsystem_admin.urls'

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

WSGI_APPLICATION = 'bookingsystem_admin.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'adminbksysdev',
        'USER': 'root',
        'PASSWORD': 'Bksysuser_2017',
        'HOST': 'mysql2704.cloudapp.net',
    },
    'rooms': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'bksysdev',
        'USER': 'root',
        'PASSWORD': 'Bksysuser_2017',
        'HOST': 'mysql2704.cloudapp.net',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

STATIC_URL = '/static/'
