from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password


class SignupSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'phone',
            'role',
            'password'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User.objects.create(
            password=make_password(password),
            **validated_data
        )

        return user