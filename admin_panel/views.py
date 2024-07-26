from django.shortcuts import render
from main.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_dashboard_stats(request):
    total_number_of_users = User.objects.count()
    number_of_subscribed_users = User.objects.exclude(subscription_id=1).count()
    number_of_standard_subscribed_users = User.objects.filter(subscription_id=2).count()
    number_of_pro_subscribed_users = User.objects.filter(subscription_id=3).count()

    data = {
        'total_number_of_users': total_number_of_users,
        'number_of_subscribed_users': number_of_subscribed_users,
        'number_of_standard_subscribed_users': number_of_standard_subscribed_users,
        'number_of_pro_subscribed_users': number_of_pro_subscribed_users
    }
    
    return Response(data)
