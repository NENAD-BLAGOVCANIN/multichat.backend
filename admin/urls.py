from django.urls import path
from .views import getDashboardStats

urlpatterns = [

    path('dashboard-stats', get_dashboard_stats, name='admin.get_dashboard_stats'),

]