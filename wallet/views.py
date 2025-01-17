from django.shortcuts import render, redirect
from rest_framework.views import APIView
from .models import Wallet
from .serializer import WalletSerializer, SumResponseSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from django.db.models import Sum, Avg
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import CustomPageNumberPagination


class ActionsList(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class WalletShortList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Берем последние 10>\
        user = request.user
        short_list = Wallet.objects.filter(user=user).order_by('-data')[:10]

        aggregation_data = Wallet.objects.filter(user=user).aggregate(
                            total_price=Sum('income_or_expence')
                            )
        total = aggregation_data['total_price']

        # Если сумма равна None (если продуктов нет), то ставим 0
        if total is None:
            total = 0

        serializer = WalletSerializer(short_list, many=True)
        # Возвращаем результат через сериализатор
        return Response({
                'records': serializer.data,
                'total': total
                }, status=status.HTTP_200_OK)

class AnonymusList(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        # Берем последние 10
        username = 'worker'
        worker = User.objects.get(username=username)
        short_list = Wallet.objects.filter(user=worker).order_by('-data')[:10]
        # Вычисляем тотал
        aggregation_data = Wallet.objects.filter(user=worker).aggregate(
            total_price=Sum('income_or_expence')
        )
        total = aggregation_data['total_price']

        # Если сумма равна None (если продуктов нет), то ставим 0
        if total is None:
            total = 0

        records_serializer = WalletSerializer(short_list, many=True)

        return Response({
                'records': records_serializer.data,
                'total': total
                }, status=status.HTTP_200_OK)


def index(request):
    return render(request, 'index.html', {'user': request.user})
