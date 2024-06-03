# from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenVerifyView
from utils.views.simplejwt import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
)


urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('painel-de-controle/', include('administration.urls')),
    path('usuario/', include('user.urls')),
    path('password/', include('resetpassword.urls')),
    path('ativos/', include('product.urls')),
    path('melhorias/', include('improvement.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # noqa: E501
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),  # noqa: E501
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include('dashboard.urls')),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
        )
