from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.account.serializers import RegisterSerializer, ForgotPasswordSerializer, \
    ForgotPasswordConfirmSerializer, ChangePasswordSerializer

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


class ForgotPasswordApiView(APIView):
    @staticmethod
    def post(request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_activation_code()
        return Response({'msg': 'Вам отправлен код активации'}, status=status.HTTP_200_OK)


class ForgotPasswordConfirmApiView(APIView):
    def post(self, request):
        serializer = ForgotPasswordConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.change_password()
        return Response({'msg': 'Пароль успешно изменен'}, status=status.HTTP_200_OK)


class ChangePasswordApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.change_password()
        return Response({'msg': 'Пароль успешно изменен'}, status=status.HTTP_200_OK)
