from rest_framework import serializers
from user.models import User
from subscription.serializers import SubscriptionSerializer

class UserSerializer(serializers.ModelSerializer):
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_subscription(self, obj):
        subscription = obj.get_subscription()
        return SubscriptionSerializer(subscription).data