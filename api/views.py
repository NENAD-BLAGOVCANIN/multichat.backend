from django.shortcuts import render, redirect
from main.models import User, Chat, MessagingService
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import datetime, timedelta
from .serializers import ChatSerializer, UserSerializer
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['username'] = user.username

        return token


@api_view(['POST'])
def createNewChat(request):
    title = request.data.get("title")
    messaging_service_name = request.data.get("messaging_service")
    messaging_service = MessagingService.objects.filter(name=messaging_service_name).first()

    chat = Chat.objects.create(title=title, messaging_service=messaging_service, user=request.user)
    session = Session.objects.create(chat=chat)
    serializer = ChatSerializer(chat, many=False, context={'request': request})

    return Response(serializer.data)

@api_view(['GET'])
def getChats(request):

    chats = Chat.objects.filter(user=request.user)

    serializer = ChatSerializer(chats, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
def deleteChat(request, chatId):

    chat = Chat.objects.get(id=chatId)
    chat.delete()

    return Response("Success")

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


@api_view(['GET'])
def getMyUserInfo(request):

    user = request.user
    serializer = UserSerializer(user, many=False, context={'request': request})

    return Response(serializer.data)
