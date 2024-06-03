from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.middleware import csrf
from typing import override


class CustomTokenObtainPairView(TokenObtainPairView):
    @override
    def post(self, request: Request, *args, **kwargs) -> Response:
        super().post(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        csrf.get_token(request)
        response = Response({'access': data['access']}, status.HTTP_200_OK)
        token = data['access']
        response = Response(
            {
                'access': token,
            },
            status.HTTP_200_OK)
        response.set_cookie(
            key='token_refresh',
            value=data.get('refresh'),
            httponly=True,
            samesite='Strict',
        )

        return response


class CustomTokenRefreshView(TokenRefreshView):
    @override
    def post(self, request: Request, *args, **kwargs) -> Response:
        data = request.data
        data["refresh"] = request.COOKIES.get('token_refresh', 'invalid token')
        serializer = self.get_serializer(data=data)
        csrf.get_token(request)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
