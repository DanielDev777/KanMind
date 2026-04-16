"""Serializers for user authentication and registration.

Provides serializers for user registration, login, and user detail display.
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user registration.

    Validates password matching and creates user with authentication token.
    """

    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'password', 'repeated_password']

    def validate(self, data):
        """Validate that password and repeated_password match."""
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        """Create a new user and generate an authentication token.

        The email is used as the username for authentication.
        """
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
    """Serializer for user login.

    Validates email and password for authentication.
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class UserDetailSerializer(serializers.ModelSerializer):
    """Read-only serializer for user info in nested objects.

    Used for displaying user details in board members, task assignees,
    reviewers, and comment authors.
    """

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']
        read_only_fields = ['id', 'email', 'fullname']