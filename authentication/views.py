from django.shortcuts import render, redirect
from user.models import User
from user.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from django.db import transaction
from django.http import HttpResponseBadRequest
from rest_framework import status
from rest_framework.authtoken.models import Token

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['username'] = user.username

        return token

@api_view(['POST'])
def registerUser(request):
    name = request.data.get("name")
    email = request.data.get("email")
    password = request.data.get("password")

    if not all([name, email, password]):
        return Response({"error": "Name, email, and password are required fields"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(email=email, username=email, password=password, name=name)
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
