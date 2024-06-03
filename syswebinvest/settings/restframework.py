from dotenv import load_dotenv
from utils.string import convert_to_string
from datetime import timedelta
import os


load_dotenv()


CORS_ALLOWED_ORIGINS = convert_to_string('CORS_ALLOWED_ORIGINS')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=float(os.environ.get('ACCESS_TOKEN_LIFETIME'))),  # type: ignore # noqa: E501
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),

    # "TOKEN_OBTAIN_SERIALIZER": "utils.serializers.simplejwt.CustomTokenObtainPairSerializer",  # noqa: E501
    "TOKEN_REFRESH_SERIALIZER": "utils.serializers.simplejwt.CustomTokenRefreshSerializer",  # noqa: E501
}
