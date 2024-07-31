from django.urls import path
from .views import createCheckoutSession, createNewChat, getUsers, updateChatPositions, editChat, getChats, deleteChat, getMyUserInfo, paymentReceived

urlpatterns = [

    path('users/', getUsers, name='api.getUsers'),
    path('users/get-my-info', getMyUserInfo, name='api.getMyUserInfo'),


    path('chats/create', createNewChat, name='api.createNewChat'),
    path('chat/<chatId>', editChat, name='api.editChat'),
    path('chats/get', getChats, name='api.getChats'),
    path('chats/delete/<chatId>', deleteChat, name='api.deleteChat'),
    path('chats/update-positions', updateChatPositions, name='api.updateChatPositions'),


    #Stripe
    path('checkout/session', createCheckoutSession, name='api.createCheckoutSession'),
    path('payments/received', paymentReceived, name='api.paymentReceived'),


]