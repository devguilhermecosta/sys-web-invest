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

PASSWORD_RESET_TIMEOUT = 14400

CSRF_TRUSTED_ORIGINS = convert_to_string('CSRF_TRUSTED_ORIGINS')

SECURE_SSL_REDIRECT = True if os.environ.get('SECURE_SSL_REDIRECT') == '1' else False

SESSION_COOKIE_SECURE = True if os.environ.get('SESSION_COOKIE_SECURE') == '1' else False

CSRF_COOKIE_SECURE = True if os.environ.get('CSRF_COOKIE_SECURE') == '1' else False
