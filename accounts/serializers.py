from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.permissions import AllowAny


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']  # или любые другие поля, которые вы хотите добавить
        extra_kwargs = {
            'password': {'write_only': True}  # Убедитесь, что пароль не будет включен в ответ
        }


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user

    # def create(self, validated_data):
    #     user = User.objects.create_user(
    #         username=validated_data['username'],
    #         email=validated_data.get('email', ''),
    #         password=validated_data['password']
    #     )
    #     return user
