from decouple import config


key_file = config('EMAIL_SSL_KEYFILE')
cert_file = config('EMAIL_SSL_CERTFILE')


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'guilherme.partic@gmail.com'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TSL = True
EMAIL_USE_SSL = True
EMAIL_SSL_KEYFILE = key_file
EMAIL_SSL_CERTFILE = cert_file
