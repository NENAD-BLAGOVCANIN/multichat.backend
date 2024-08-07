from django.shortcuts import render, redirect
from user.models import User
from chat.models import Chat, MessagingService
from subscription.models import Subscription
from payment.models import Payment
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from datetime import datetime, timedelta
from chat.serializers import ChatSerializer
from user.serializers import UserSerializer
from rest_framework import status
import stripe
from django.conf import settings
from django.db import transaction
from django.http import HttpResponseBadRequest


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
                'price': 'price_1PjeEwAHonOpKVtAopa6MBC5',
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url='https://multi-chat.io/payment/success', 
        cancel_url='https://multi-chat.io',
    )

    return redirect(checkout_session.url)


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