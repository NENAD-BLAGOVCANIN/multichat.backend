from rest_framework import serializers
from .models import Subscription, UserSubscription

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class UserSubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = UserSubscription
        fields = '__all__'

    def get_user(self, obj):
        from user.serializers import UserSerializer
        return UserSerializer(obj.user).data