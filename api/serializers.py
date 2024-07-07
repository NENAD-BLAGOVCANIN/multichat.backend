from rest_framework import serializers
from main.models import Chat, MessagingService, User, Subscription

class MessagingServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessagingService
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class ChatSerializer(serializers.ModelSerializer):
    messaging_service = MessagingServiceSerializer()

    class Meta:
        model = Chat
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer()

    class Meta:
        model = User
        fields = '__all__'