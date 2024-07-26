from django.urls import path
from .views import get_dashboard_stats, get_monthly_earnings

urlpatterns = [

    path('dashboard-stats/', get_dashboard_stats, name='admin.get_dashboard_stats'),
    path('dashboard-stats/monthly-earnings', get_monthly_earnings, name='admin.get_monthly_earnings'),

]