from django.shortcuts import render, redirect
from main.models import User, Chat, MessagingService, Subscription, Payment
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from datetime import datetime, timedelta
from .serializers import ChatSerializer, UserSerializer
from rest_framework import status
from django.contrib.auth import authenticate, login
import stripe
from django.conf import settings
from django.db import transaction
from django.http import HttpResponseBadRequest


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
def createCheckoutSession(request):

    user_id = request.data.get("user_id")
    user = User.objects.get(id=user_id)

    stripe.api_key = settings.STRIPE_API_KEY

    customer = stripe.Customer.create(
        email=user.email
    )

    checkout_session = stripe.checkout.Session.create(
        customer=customer.id,
        payment_method_types=['card'],
        line_items=[
            {
                'price': 'price_1PZMfgAHonOpKVtAX4HAfvCx',
                'quantity': 1,
            },
        ],
        mode='payment',
    )

    return Response(checkout_session.url)


@api_view(['POST'])
def paymentReceived(request):

    stripe.api_key = settings.STRIPE_API_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET

    payload = request.body.decode('utf-8')
    sig_header = request.headers.get('STRIPE_SIGNATURE', '')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponseBadRequest(f"Invalid payload: {str(e)}")
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponseBadRequest(f"Invalid signature: {str(e)}")

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        user_email = session['customer_details']['email']
        user = User.objects.filter(email=user_email).first()

        stripe_payment_link = session['payment_link']
        subscription = Subscription.objects.filter(stripe_payment_link=stripe_payment_link).first()

        user.subscription = subscription
        user.save()

        payment = Payment(amount=subscription.cost, user=user)
        payment.save()

        return Response({"message": "Subscription created successfully."})

    elif event['type'] == 'customer.subscription.deleted':
        subscription_id = event['data']['object']['id']
        user = User.objects.filter(subscription__stripe_subscription_id=subscription_id).first()
        subscription = Subscription.objects.get(id=1).first()

        if user:
            user.subscription = subscription
            user.save()
            return Response({"message": "Subscription cancelled successfully."})

    else:
        print('Unhandled event type {}'.format(event['type']))

    return Response({"message": "Event received"})

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


@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)