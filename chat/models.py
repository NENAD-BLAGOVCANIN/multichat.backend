from django.db import models
from user.models import User
from common.models import BaseModel


class MessagingService(BaseModel):
    title = models.CharField(max_length=50, default="WhatsApp")
    url = models.CharField(max_length=150, default="https://web.whatsapp.com/")
    name = models.CharField(max_length=50, default="whatsapp")
    description = models.CharField(max_length=355)
    icon = models.CharField(max_length=355, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "messaging_service"

class Chat(BaseModel):
    title = models.CharField(max_length=255)
    messaging_service = models.ForeignKey(MessagingService, default=None, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    notifications = models.BooleanField(default=True)
    audio_notifications = models.BooleanField(default=True)
    position = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "chat"
        ordering = ['position']
