import os
from dotenv import load_dotenv


load_dotenv()

use_ssl = True if os.environ.get('EMAIL_USE_SSL') == '1' else False
key_file = os.environ.get('EMAIL_SSL_KEYFILE', None)
cert_file = os.environ.get('EMAIL_SSL_CERTFILE', None)


EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TSL = False
EMAIL_USE_SSL = use_ssl
EMAIL_SSL_KEYFILE = key_file
EMAIL_SSL_CERTFILE = cert_file
