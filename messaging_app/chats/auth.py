from rest_framework.views import APIView
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import get_user_model


User = get_user_model


class CostomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]


class CostomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]


class LogoutView(APIView):

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):

    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')

        if not email or not password or not username:
            return Response({"Error: Incorect username or password"},
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email.exist()):
            return Response({"Error: Email already exist"},
                            status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(
            email=email,
            password=password,
            username=username,
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )
        return Response({'Message: User created succesfully'},
                        status=status.HTTP_201_CREATED)
