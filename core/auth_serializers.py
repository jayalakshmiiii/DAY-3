from rest_framework import serializers
from .models import User


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
            **validated_data
        )

        user.password = password
        user.save()

        return user