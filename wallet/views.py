from django.shortcuts import render
from rest_framework.views import APIView
from .models import Wallet
from .serializer import WalletSerializer
from rest_framework.response import Response
from rest_framework import viewsets


class ActionsList(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


def index(request):
    return render(request, 'index.html')
