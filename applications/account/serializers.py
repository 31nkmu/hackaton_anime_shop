from django.contrib.auth import get_user_model
from rest_framework import serializers

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

    def validate_email(self, email):
        if User.objects.filter(email=email):
            raise serializers.ValidationError('Такой пользователь уже существует')
        return email

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        user = User.objects.create_user(email=email,
                                        password=password)
        from applications.account.tasks import send_activation_link
        send_activation_link.delay(email, user.activation_code)
        return user
