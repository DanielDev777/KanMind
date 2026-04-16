"""API views for user authentication.

Provides endpoints for user registration, login, logout, and email checking.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from auth_app.models import CustomUser


class RegisterView(APIView):
    """Handle user registration.

    Create a new user account and return an authentication token.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """Register a new user and return authentication token."""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                token = Token.objects.get(user=user)

                return Response({
                    'token': token.key,
                    'fullname': user.fullname,
                    'email': user.email,
                    'user_id': user.id
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                import traceback
                return Response(
                    {'error': str(e), 'traceback': traceback.format_exc()},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Handle user login.

    Authenticate user credentials and return an authentication token.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """Authenticate user and return token."""
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = authenticate(request, username=email, password=password)

                if user is not None:
                    token, created = Token.objects.get_or_create(user=user)

                    return Response({
                        'token': token.key,
                        'fullname': user.fullname,
                        'email': user.email,
                        'user_id': user.id
                    }, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {'error': 'Invalid credentials'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except Exception as e:
                return Response(
                    {'error': 'Internal server error'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """Handle user logout.

    Delete the user's authentication token.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Delete the user's authentication token."""
        request.user.auth_token.delete()
        return Response({"detail": "Logout erfolgreich. Token wurde gelöscht."}, status=status.HTTP_200_OK)


class EmailCheckView(APIView):
    """Check if an email exists in the database.

    Used for validating user emails before board invitations.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Check if email exists and return user data if found."""
        email = request.query_params.get('email')
        if not email:
            return Response({'error': 'Email is missing or has the wrong format.'}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.filter(email=email).first()

        if user:
            return Response({"id": user.id, "email": user.email, "fullname": user.fullname}, status=status.HTTP_200_OK)
        return Response(f'User with email {email} was not found', status=status.HTTP_404_NOT_FOUND)
