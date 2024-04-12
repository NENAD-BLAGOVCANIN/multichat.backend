from django.shortcuts import render, redirect
from main.models import User, Chat, MessagingService
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import datetime, timedelta

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['username'] = user.username

        return token


def createNewChat(request):

    title = request.get("title")
    messaging_service = request.get("messaging_service")

    chat = Chat.objects.create(title = title, messaging_service = messaging_service)
    chat.save()

    return Response(chat)

