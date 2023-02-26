from pathlib import Path
import os
import environ
import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_21_9")

# READ Environment variables
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'drf_spectacular',
    'movies'
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

ROOT_URLCONF = 'app.urls'

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

WSGI_APPLICATION = 'app.wsgi.application'

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': env("DB_NAME"),
    #     'USER': env("DB_USER"),
    #     'PASSWORD': env("DB_PASSWORD"),
    #     'HOST': env("DB_HOST"),
    #     'PORT': env("DB_PORT"),
    # }
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': '127.0.0.1:1521/orcl',
        'USER': 'system',
        'PASSWORD': 'admin',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    # Below disables the default UI for Django rest framework
    # 'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny', ],
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.TokenAuthentication', ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '100/day',
        'review-create-throttle': '2/day',
        'review-list-throttle': '100/day',
        'review-detail-throttle': '100/day',
    },
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Movie Ratings API',
    'DESCRIPTION': 'API for Movie Ratings',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
