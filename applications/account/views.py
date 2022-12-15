from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.account.serializers import RegisterSerializer

User = get_user_model()


class RegisterApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ActivationApiView(APIView):
    def get(self, request, activation_code):
        user = User.objects.filter(activation_code=activation_code)
        if not user.exists():
            return Response({'msg': 'Неверный код активации'}, status=status.HTTP_400_BAD_REQUEST)
        user = user[0]
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response({'msg': 'Ваш аккаунт успешно активирован'}, status=status.HTTP_200_OK)
        #
        # try:
        #     user = User.objects.get(activation_code=activation_code)
        #     user.is_active = True
        #     user.activation_code = ''
        #     user.save()
        #     return Response()
        # except User.DoesNotExist:
        #     return Response()
