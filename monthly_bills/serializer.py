from rest_framework import serializers
from .models import MonthlyBills

class MonthlyBillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyBills
        fields = (
            'bill_name',
            'rate',
            'date_to_pay',
            'paid'
        )