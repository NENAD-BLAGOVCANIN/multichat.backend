from django.urls import path
from .views import createCheckoutSession, paymentReceived, paymentSuccess, get_my_payments

urlpatterns = [

    #Stripe
    path('payments/create-checkout-session', createCheckoutSession, name='payment.createCheckoutSession'),
    path('payments/received', paymentReceived, name='payment.paymentReceived'),
    path('payments/success', paymentSuccess, name='payment.paymentSuccess'),
    path('payments/my-payments', get_my_payments, name='payment.get_my_payments'),

]