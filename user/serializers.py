from rest_framework import serializers
from user.models import User
from subscription.serializers import SubscriptionSerializer


class UserSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer()

    class Meta:
        model = User
        fields = '__all__'