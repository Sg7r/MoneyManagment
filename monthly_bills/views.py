from django.shortcuts import render
from rest_framework import viewsets
from .models import MonthlyBills
from .serializer import MonthlyBillsSerializer


class MonthlyBillsList(viewsets.ModelViewSet):
    queryset = MonthlyBills.objects.all()
    serializer_class = MonthlyBillsSerializer
