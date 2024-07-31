from django.db import models
from common.models import BaseModel


class Subscription(BaseModel):
    title = models.CharField(max_length=50, default="WhatsApp")
    stripe_payment_link = models.CharField(max_length=200, blank=True)
    cost = models.IntegerField(default=0)
    max_tabs = models.IntegerField(default=5, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "subscription"