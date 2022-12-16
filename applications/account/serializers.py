from django.contrib.auth import get_user_model
from rest_framework import serializers

from applications.account import tasks

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(min_length=6, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']

    def validate(self, attrs):
        p1 = attrs['password']
        p2 = attrs['password2']
        if p1 != p2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    @staticmethod
    def validate_email(email):
        if User.objects.filter(email=email):
            raise serializers.ValidationError('Такой пользователь уже существует')
        return email

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        user = User.objects.create_user(email=email,
                                        password=password)
        tasks.send_activation_link.delay(email, user.activation_code)
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)

    @staticmethod
    def validate_email(email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Нет такого зарегистрированного пользователя')
        return email

    def send_activation_code(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        user.save()
        tasks.send_code.delay(email, user.activation_code)


class ForgotPasswordConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)
    new_password = serializers.CharField(min_length=6, required=True)
    new_password_confirm = serializers.CharField(min_length=6, required=True)

    @staticmethod
    def validate_email(email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Нет такого зарегистрированного пользователя')
        return email

    @staticmethod
    def validate_code(code):
        if not User.objects.filter(activation_code=code):
            raise serializers.ValidationError('Неправильный код активации')
        return code

    def validate(self, attrs):
        p1 = attrs['new_password']
        p2 = attrs['new_password_confirm']
        if p1 != p2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def change_password(self):
        password = self.validated_data['new_password']
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        user.set_password(password)
        user.activation_code = ''
        user.save()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, min_length=6)
    new_password = serializers.CharField(required=True, min_length=6)
    new_password_confirm = serializers.CharField(required=True, min_length=6)

    def validate(self, attrs):
        p1 = attrs['new_password']
        p2 = attrs['new_password_confirm']
        if p1 != p2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def validate_old_password(self, old_password):
        user = self.context.get('user')
        if not user.check_password(old_password):
            raise serializers.ValidationError('Старый пароль введен неверно')
        return old_password

    def change_password(self):
        user = self.context.get('user')
        password = self.validated_data['new_password']
        user.set_password(password)
        user.save()
