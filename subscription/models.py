from django.db import models
from common.models import BaseModel
from django.utils import timezone
from datetime import timedelta
from user.models import User

class Subscription(BaseModel):
    title = models.CharField(max_length=50, default="WhatsApp")
    stripe_payment_link = models.CharField(max_length=200, blank=True)
    cost = models.IntegerField(default=0)
    max_tabs = models.IntegerField(default=5, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "subscription"

class UserSubscription(BaseModel):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, null=True, on_delete=models.CASCADE)
    renewal_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.renewal_date:
            self.renewal_date = timezone.now() + timedelta(days=30)
        super(UserSubscription, self).save(*args, **kwargs)

    class Meta:
        db_table = "user_subscription"