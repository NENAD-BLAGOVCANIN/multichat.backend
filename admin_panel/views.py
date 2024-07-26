from django.shortcuts import render
from main.models import User, Payment, MessagingService
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from datetime import timedelta
from django.db.models.functions import TruncMonth
from django.utils import timezone
from api.serializers import MessagingServiceSerializer

@api_view(['GET'])
def get_dashboard_stats(request):
    total_number_of_users = User.objects.count()
    number_of_subscribed_users = User.objects.exclude(subscription_id=1).count()
    number_of_standard_subscribed_users = User.objects.filter(subscription_id=2).count()
    number_of_pro_subscribed_users = User.objects.filter(subscription_id=3).count()


    total_earnings = Payment.objects.aggregate(total=Sum('amount'))['total']
    
    if total_earnings is None:
        total_earnings = 0

    data = {
        'total_number_of_users': total_number_of_users,
        'number_of_subscribed_users': number_of_subscribed_users,
        'number_of_standard_subscribed_users': number_of_standard_subscribed_users,
        'number_of_pro_subscribed_users': number_of_pro_subscribed_users,
        'total_earnings': total_earnings
    }
    
    return Response(data)

@api_view(['GET'])
def get_monthly_earnings(request):
    now = timezone.now()
    one_year_ago = now - timedelta(days=365)

    monthly_earnings = (
        Payment.objects
        .filter(created_at__gte=one_year_ago)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total_earnings=Sum('amount'))
        .order_by('month')
    )

    month_names = []
    earnings = []
    for i in range(12):
        month = (now - timedelta(days=30 * (11 - i))).strftime('%B %Y')
        month_names.append(month)
        earnings.append(0)

    earnings_map = {entry['month'].strftime('%B %Y'): entry['total_earnings'] for entry in monthly_earnings}
    for i, month in enumerate(month_names):
        if month in earnings_map:
            earnings[i] = earnings_map[month]

    data = {
        'months': month_names,
        'earnings': earnings,
    }

    return Response(data)

@api_view(['GET'])
def get_messaging_services(request):
    messaging_services = MessagingService.objects.all()
    serializer = MessagingServiceSerializer(messaging_services, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_subscriptions(request):
    subscriptions = User.objects.exclude(subscription_id=1)
    serializer = User(subscriptions, many=True)
    return Response(serializer.data)