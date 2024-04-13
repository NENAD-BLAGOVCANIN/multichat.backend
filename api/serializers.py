from rest_framework import serializers
from main.models import Chat, MessagingService

class MessagingServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessagingService
        fields = '__all__'

class ChatSerializer(serializers.ModelSerializer):
    messaging_service = MessagingServiceSerializer()

    class Meta:
        model = Chat
        fields = '__all__'