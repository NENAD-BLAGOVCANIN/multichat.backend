from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import createNewChat, getChats, deleteChat

urlpatterns = [

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('chats/create', createNewChat, name='api.createNewChat'),
    path('chats/get', getChats, name='api.getChats'),
    path('chats/delete/<chatId>', deleteChat, name='api.deleteChat'),

]