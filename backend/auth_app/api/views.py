from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
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
    permission_classes = [AllowAny]
    
    def post(self, request):
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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "Logout erfolgreich. Token wurde gelöscht."}, status=status.HTTP_200_OK)