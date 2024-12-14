"""
Django settings for pcshop project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import dj_database_url
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import os

# Load backend.env
load_dotenv(find_dotenv("backend.env"))

# Load postgres.env
load_dotenv(find_dotenv("postgres.env"))


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = (
    os.getenv("ALLOWED_HOSTS", "*").split(" ") if os.getenv("ALLOWED_HOSTS") else ["*"]
)


LOGOUT_REDIRECT_URL = "/"
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/login/"

SESSION_COOKIE_AGE = 86400
CART_SESSION_ID = "cart"


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "cart",
    "core",
    "order",
    "product.apps.ProductConfig",
    "algoliasearch_django",
    "django_jalali",
    "django_jalali.db",
    "django.contrib.humanize",
    "storages",
    "django_browser_reload",
    "api",
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
]


ALGOLIA = {
    "APPLICATION_ID": os.getenv("ALGO_APPLICATION_ID"),
    "API_KEY": os.getenv("ALGOLIA_KEY"),
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]


# Allow specific origins
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5500",  # If running HTML from a local server
    # "http://localhost:3000", #  for React/Node.js
    # "http://127.0.0.1:8000", #  for Django development server
]


ROOT_URLCONF = "pcshop.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "cart.context_processors.cart",
            ],
        },
    },
]

WSGI_APPLICATION = "pcshop.wsgi.application"


# Database configuration
DATABASE_URL = os.environ.get("DB_URL")

if DATABASE_URL:
    # Use PostgreSQL if DB_URL is set
    DATABASES = {"default": dj_database_url.config(default=DATABASE_URL)}
else:
    # Fall back to SQLite if DB_URL is not set
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "fa-ir"  # Persian language
TIME_ZONE = "Asia/Tehran"  # Iran's time zone

USE_I18N = True
USE_L10N = True
USE_TZ = True

FILE_CHARSET = "utf-8"
DEFAULT_CHARSET = "utf-8"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media/"
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# settings.py
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# S3 Settings
LIARA_ENDPOINT = os.getenv("LIARA_ENDPOINT")
LIARA_BUCKET_NAME = os.getenv("LIARA_BUCKET_NAME")
LIARA_ACCESS_KEY = os.getenv("LIARA_ACCESS_KEY")
LIARA_SECRET_KEY = os.getenv("LIARA_SECRET_KEY")

# S3 Settings Based on AWS (optional)
AWS_ACCESS_KEY_ID = LIARA_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = LIARA_SECRET_KEY
AWS_STORAGE_BUCKET_NAME = LIARA_BUCKET_NAME
AWS_S3_ENDPOINT_URL = LIARA_ENDPOINT
AWS_S3_REGION_NAME = "us-east-1"

# Django-storages configuration
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
