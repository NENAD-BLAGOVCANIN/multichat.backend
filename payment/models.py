from django.db import models
from user.models import User
from common.models import BaseModel

class Payment(BaseModel):

    amount = models.IntegerField(default=0)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "payment"