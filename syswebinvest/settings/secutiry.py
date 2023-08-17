import os
from utils.string import convert_to_string
from dotenv import load_dotenv


load_dotenv()


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = convert_to_string('ALLOWED_HOSTS')

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

PASSWORD_RESET_TIMEOUT = os.environ.get('PASSWORD_RESET_TIMEOUT')

CSRF_TRUSTED_ORIGINS = convert_to_string('CSRF_TRUSTED_ORIGINS')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'guilherme.partic@gmail.com'
EMAIL_HOST_PASSWORD = 'slatnkhovazmjkev'
EMAIL_SSL_CERTFILE = '~/etc/letsencrypt/live/euinvestidor.devguilhermecosta.com/fullchain.pem'
