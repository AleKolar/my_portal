"""
Django settings for my_portal project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path
import logging.handlers
import smtplib
from email.message import EmailMessage
import email.utils
import ssl

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-33%y9_g%z6hb1^3t$8d105#8_*%4*edtz@@&bzk=nixg&=sgat'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

SITE_ID = 1

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

LANGUAGE_CODE = 'ru'

LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
)

INSTALLED_APPS = [
    'modeltranslation',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'news',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django_filters',
    'protect',
    'sign',
    'allauth.socialaccount.providers.google',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_apscheduler',

    'django.contrib.humanize',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.locale.LocaleMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'allauth.account.middleware.AccountMiddleware',

    'news.basic.middlewares.TimezoneMiddleware',

]

ROOT_URLCONF = 'my_portal.urls'

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
                'django.template.context_processors.request',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [

    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'my_portal.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_my_portal.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_URL = 'static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

LOGIN_URL = 'sign/login/'

LOGIN_REDIRECT_URL = 'protect/'

LOGOUT_REDIRECT_URL = 'logout/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = ("mandatory")
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = 'confirm_email'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': 'ваш_client_id',
            'secret': 'ваш_client_secret',
        }
    }
}

ACCOUNT_FORMS = {'signup': 'sign.models.BasicSignupForm'}

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'gefest-173'
EMAIL_HOST_PASSWORD = 'Mn14071979'
EMAIL_USE_SSL = True

context = ssl.create_default_context()
context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Exclude TLS 1.0 and 1.1
context.minimum_version = ssl.TLSVersion.TLSv1_2  # Specify TLS 1.2 as the minimum version

# Connect to the SMTP server using the specified SSL context
with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=context) as server:
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# import environ
# env = environ.Env()
# DEFAULT_FROM_EMAIL = env.str('MY_PASSWORD')

DEFAULT_FROM_EMAIL = 'Mn14071979'

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 20

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"

APSCHEDULER_RUN_NOW_TIMEOUT = 25

CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'

CELERY_RESULT_BACKEND = 'rpc://'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
    }
}

'''
Я смог сделать logging требуемой конфигурации файла журнала, 
только, при помощи конструктора basicConfig(),без явной ссылки на 'my_portal'
'''

# LOGS_DIR = os.path.join(BASE_DIR, 'logs')
#
# logging.basicConfig(level=logging.DEBUG)
#
# file_general_handler = logging.FileHandler(os.path.join(LOGS_DIR, 'general.log'))
# file_general_handler.setLevel(logging.INFO)
# file_general_format = logging.Formatter('%(levelname)s %(asctime)s %(module)s %(message)s')
# file_general_handler.setFormatter(file_general_format)
#
# file_errors_handler = logging.FileHandler(os.path.join(LOGS_DIR, 'errors.log'))
# file_errors_handler.setLevel(logging.ERROR)
# file_errors_format = logging.Formatter('%(levelname)s %(asctime)s %(module)s %(message)s %(pathname)s')
# file_errors_handler.setFormatter(file_errors_format)
#
# file_security_handler = logging.FileHandler(os.path.join(LOGS_DIR, 'security.log'))
# file_security_handler.setLevel(logging.INFO)
# file_security_handler.addFilter(logging.Filter('django.security'))
# file_security_format = logging.Formatter('%(levelname)s %(asctime)s %(module)s %(message)s')
# file_security_handler.setFormatter(file_security_format)
#
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)
# console_format = logging.Formatter('%(levelname)s %(asctime)s %(pathname)s %(module)s %(message)s')
# console_handler.setFormatter(console_format)
#
#
# class SSLSMTPHandler(logging.handlers.SMTPHandler):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.server = smtplib.SMTP_SSL(self.mailhost, context=self.secure)
#
#     def emit(self, record):
#         try:
#             msg = EmailMessage()
#             msg['From'] = self.fromaddr
#             msg['To'] = ','.join(self.toaddrs)
#             msg['Subject'] = self.getSubject(record)
#             msg['Date'] = email.utils.localtime()
#             msg.set_content(self.format(record))
#             if self.username:
#                 self.server.login(self.username, self.password)
#             self.server.send_message(msg, self.fromaddr, self.toaddrs)
#         except (KeyboardInterrupt, SystemExit):
#             raise
#
#
# email_admins_handler = SSLSMTPHandler(
#     mailhost=EMAIL_HOST,
#     fromaddr='gefest-173@yandex.ru',
#     toaddrs=['alek.kolark@gmail.com', 'alekolar17982@gmail.com'],
#     subject='Error in app',
#     credentials=(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD),
#     secure=context
# )
# email_admins_handler.setLevel(logging.ERROR)
# email_admins_handler.setFormatter(logging.Formatter('%(levelname)s %(asctime)s %(module)s %(message)s'))
#
# root_logger = logging.getLogger('')
# root_logger.addHandler(file_general_handler)
# root_logger.addHandler(file_errors_handler)
# root_logger.addHandler(file_security_handler)
# root_logger.addHandler(email_admins_handler)
# root_logger.addHandler(console_handler)
#
# root_logger.setLevel(logging.DEBUG)
#
# root_logger.error("Test error message")
