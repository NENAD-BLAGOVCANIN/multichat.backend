from django.urls import path
from .views import createNewChat, updateChatPositions, editChat, getChats, deleteChat

urlpatterns = [

    path('chats/create', createNewChat, name='chat.createNewChat'),
    path('chat/<chatId>', editChat, name='chat.editChat'),
    path('chats/get', getChats, name='chat.getChats'),
    path('chats/delete/<chatId>', deleteChat, name='chat.deleteChat'),
    path('chats/update-positions', updateChatPositions, name='chat.updateChatPositions'),

]