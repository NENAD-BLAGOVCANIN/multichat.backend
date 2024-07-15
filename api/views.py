from django.shortcuts import render, redirect
from main.models import User, Chat, MessagingService, Subscription
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
import stripe
from django.conf import settings

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['username'] = user.username

        return token

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

    chat = Chat.objects.create(title=title, messaging_service=messaging_service, user=request.user)
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


def userHasMaxTabs(user):

    existing_users_tabs_count = Chat.objects.filter(user=user, is_deleted=0).count()
    allowed_no_of_tabs = user.subscription.max_tabs

    print(existing_users_tabs_count)
    print(allowed_no_of_tabs)

    if(existing_users_tabs_count==allowed_no_of_tabs):
        return True

    return False

@api_view(['POST'])
def paymentReceived(request):

    stripe.api_key = settings.STRIPE_API_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET


    event = None
    payload = request.body.decode('utf-8')
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
    # ... handle other event types
    else:
      print('Unhandled event type {}'.format(event['type']))

    user_email = event['data']['object']['customer_details']['email']
    user = User.objects.filter(email=user_email).first()

    stripe_product_id = event['data']['object']['id']
    subscription = Subscription.objects.filter(stripe_id=stripe_product_id).first()

    user.subscription = subscription
    user.save()

    return Response({"message": str(stripe_product_id)})
