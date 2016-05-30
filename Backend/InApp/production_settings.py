"""
Django settings for InApp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p3_df(so=$d8p79ew@jp)&yae+mdul63ae7%1aok2v0m^7c4n@'
DOMAIN = 'http://inapptranslation.com/'
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
    'rest_framework',
    'rest_framework.authtoken',
    'api',
    'corsheaders',
    'django.contrib.sites',
)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    ),
}
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'api.middleware.RequestLogger'
)

ROOT_URLCONF = 'InApp.urls'

WSGI_APPLICATION = 'InApp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'inapp',
        'USER': 'inapp',
        'PASSWORD': 'inappinapp',
        'HOST': 'inapp.cfluym4ogs0x.ap-northeast-1.rds.amazonaws.com'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/api/static/'

STATIC_ROOT = "/usr/local/virtualenvs/InApp/InAppTranslation_Server/static/"

AUTH_USER_MODEL = 'api.User'

CORS_ORIGIN_ALLOW_ALL = True

APPEND_SLASH = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'mizutori@gmail.com'
EMAIL_HOST_PASSWORD = 'w3v-PGcD5GMa6ERKW_gYfw'
SITE_ID = 1

SUPPORT_EMAIL = 'mizutori@gmail.com'
GENGO_PUBLIC_KEY = '{6r-l$8r@kF7=0zu=Y^BB_2mcfFBbAZ9gSbPuQ$26_bDN$hv39sh=_9fBF|}}E^)'
GENGO_PRIVATE_KEY = 'cefIQ{2KJP_paeE2LYsi^3yS_wf|VRo~7WV8P(cQl^VjHjy]O-=4SyW6]Wv3sD}g'
GENGO_SANDBOX = True
GENGO_DEBUG = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'