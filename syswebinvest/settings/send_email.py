import os
from dotenv import load_dotenv


load_dotenv()


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'guilherme.partic@gmail.com'
EMAIL_HOST_PASSWORD = 'slatnkhovazmjkev'
