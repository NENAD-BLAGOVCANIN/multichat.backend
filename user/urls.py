from django.urls import path
from .views import getUsers, getMyUserInfo

urlpatterns = [

    path('users/', getUsers, name='user.getUsers'),
    path('users/get-my-info', getMyUserInfo, name='user.getMyUserInfo'),

]