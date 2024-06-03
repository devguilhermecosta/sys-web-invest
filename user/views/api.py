from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import AbstractBaseUser
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from ..serializers import UserSerializer


class UserRegisterAPIVire(APIView):
    def post(self, *args, **kwargs) -> Response:
        serializer = UserSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        pk = serializer.validated_data.get('id')
        password = serializer.validated_data.get('password')
        user_model = get_user_model()

        registered_user = user_model.objects.filter(pk=pk).first()

        if registered_user:
            registered_user.set_password(password)
            registered_user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk: int) -> AbstractBaseUser:
        model = get_user_model()
        user = get_object_or_404(
            model,
            pk=pk
        )
        return user

    def get(self, *args, **kwargs) -> Response:
        pk = kwargs.get('pk', '')
        user = self.get_object(pk)
        serializer = UserSerializer(instance=user)
        data = {k: v for k, v in serializer.data.items() if k != 'password'}
        return Response(
            data=data,
            status=status.HTTP_200_OK,
        )

    @method_decorator(csrf_protect)
    def patch(self, *args, **kwargs) -> None:
        ...


class UserListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_model = get_user_model()
        user_list = user_model.objects.all()
        return user_list

    def get(self, *args, **kwargs) -> Response:
        user_list = self.get_object()
        serializer = UserSerializer(
            instance=user_list,
            many=True,
        )

        data = [
            {k: v for k, v in user.items() if k != 'password'}
            for user in serializer.data
        ]

        return Response(
            data=data,
            status=status.HTTP_200_OK,
        )


# TODO - continuar pelo método patch
