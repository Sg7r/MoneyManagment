from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Wallet(models.Model):
    income_or_expence = models.DecimalField(max_digits=10, decimal_places=2)
    target = models.TextField()
    current_balance = models.SmallIntegerField(blank=True, null=True)
    data = models.DateTimeField(default=datetime.now())
    user = models.ForeignKey(User, on_delete=models.CASCADE)
