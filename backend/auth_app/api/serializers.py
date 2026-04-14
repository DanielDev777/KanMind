from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'password', 'repeated_password']

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('repeated_password')
        
        validated_data['username'] = validated_data['email']

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            fullname=validated_data.get('fullname', '')
        )

        Token.objects.create(user=user)

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class UserDetailSerializer(serializers.ModelSerializer):
    """Read-only serializer for user info in nested objects (members, assignees, etc.)"""
    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']
        read_only_fields = ['id', 'email', 'fullname']