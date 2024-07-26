from django.urls import path
from .views import get_dashboard_stats, get_monthly_earnings, get_messaging_services, get_subscriptions

urlpatterns = [

    path('dashboard-stats/', get_dashboard_stats, name='admin.get_dashboard_stats'),
    path('earnings/', get_monthly_earnings, name='admin.get_monthly_earnings'),
    path('messaging-services/', get_messaging_services, name='admin.get_messaging_services'),
    path('subscriptions/', get_subscriptions, name='admin.get_subscriptions'),

]