from django.urls import path
from .views import get_dashboard_stats, get_monthly_earnings, get_messaging_services

urlpatterns = [

    path('dashboard-stats/', get_dashboard_stats, name='admin.get_dashboard_stats'),
    path('earnings/', get_monthly_earnings, name='admin.get_monthly_earnings'),
    path('messaging-services/', get_messaging_services, name='admin.get_messaging_services'),

]