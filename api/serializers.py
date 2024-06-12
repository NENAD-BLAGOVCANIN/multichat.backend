from rest_framework import serializers
from main.models import Chat, MessagingService, User

class MessagingServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessagingService
        fields = '__all__'

class ChatSerializer(serializers.ModelSerializer):
    messaging_service = MessagingServiceSerializer()

    class Meta:
        model = Chat
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'