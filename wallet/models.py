from django.db import models
from datetime import datetime


class Wallet(models.Model):
    income_or_expence = models.SmallIntegerField()
    target = models.TextField()
    current_balance = models.SmallIntegerField(blank=True, null=True)
    data = models.DateTimeField(default=datetime.now())
