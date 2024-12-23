from django.db import models
from datetime import datetime


class Wallet(models.Model):
    income_or_expence = models.SmallIntegerField()
    target = models.TextField()
    current_balance = models.SmallIntegerField()
    data = models.DateTimeField(default=datetime.now())
