from django.db import models
from datetime import datetime

class MonthlyBills(models.Model):
    bill_name = models.TextField()
    rate = models.SmallIntegerField()
    date_to_pay = models.DateTimeField(default=datetime.now())
    paid = models.BooleanField()

