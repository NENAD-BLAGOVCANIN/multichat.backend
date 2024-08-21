from django.shortcuts import render, redirect
from user.models import User
from chat.models import Chat, MessagingService
from subscription.models import Subscription
from payment.models import Payment
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from datetime import datetime, timedelta
from .serializers import ChatSerializer
from user.serializers import UserSerializer
from rest_framework import status
from django.contrib.auth import authenticate, login
import stripe
from django.conf import settings
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.db.models import Max


@api_view(['POST'])
def createNewChat(request):

    user = request.user

    if userHasMaxTabs(user):
        return Response(
            {"detail": "You have reached the maximum number of tabs allowed."},
            status=status.HTTP_403_FORBIDDEN
        )

    title = request.data.get("title")
    messaging_service_name = request.data.get("messaging_service")
    messaging_service = MessagingService.objects.filter(name=messaging_service_name).first()
    max_position = Chat.objects.filter(user=user).aggregate(Max('position'))['position__max'] or 0
    chat = Chat.objects.create(
        title=title,
        messaging_service=messaging_service,
        user=user,
        position=max_position + 1
    )
    serializer = ChatSerializer(chat, many=False, context={'request': request})

    return Response(serializer.data)

@api_view(['PUT'])
def editChat(request, chatId):
    title = request.data.get("title")
    audio_notifications = request.data.get("audio_notifications")
    notifications = request.data.get("notifications")

    chat = Chat.objects.get(id=chatId)
    chat.title = title
    chat.audio_notifications = audio_notifications
    chat.notifications = notifications
    chat.save()
    
    serializer = ChatSerializer(chat, many=False, context={'request': request})

    return Response(serializer.data)

@api_view(['GET'])
def getChats(request):

    chats = Chat.objects.filter(user=request.user).order_by('position')

    serializer = ChatSerializer(chats, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
def deleteChat(request, chatId):

    chat = Chat.objects.get(id=chatId)
    chat.delete()

    return Response("Success")


def userHasMaxTabs(user):

    existing_users_tabs_count = Chat.objects.filter(user=user, is_deleted=0).count()
    allowed_no_of_tabs = 5

    print(existing_users_tabs_count)
    print(allowed_no_of_tabs)

    if(existing_users_tabs_count==allowed_no_of_tabs):
        return True

    return False

@api_view(['POST'])
def updateChatPositions(request):
    user = request.user
    positions = request.data.get('positions', [])

    with transaction.atomic():
        for pos in positions:
            chat_id = pos.get('id')
            position = pos.get('position')
            Chat.objects.filter(id=chat_id, user=user).update(position=position)
    
    return Response({"detail": "Positions updated successfully."}, status=status.HTTP_200_OK)
