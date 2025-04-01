from django.shortcuts import render, redirect
from rest_framework.views import APIView
from .models import Wallet
from .serializer import WalletSerializer, AnonymousSerializer, SumResponseSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from django.db.models import Sum, Avg
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db.models import Q
from .tasks import delete_anonymous_records
from datetime import datetime, timedelta
from django.utils import timezone
from .filters import WalletFilter
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from .pagination import CustomPageNumberPagination


class ActionsList(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class AnonymousList(viewsets.ModelViewSet):
    permission_classes = []
    authentication_classes = []

    queryset = Wallet.objects.all()
    serializer_class = AnonymousSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.user_id is None:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_403_FORBIDDEN)


class WalletList(APIView):
    permission_classes = [IsAuthenticated]

    pagination_class = CustomPageNumberPagination
    filterset_class = WalletFilter

    def apply_filters(self, request, queryset):
        """Применяем фильтры вручную."""
        filter_backend = DjangoFilterBackend()
        # Применяем фильтрацию с помощью filterset_class
        return filter_backend.filter_queryset(request, queryset, self)

    def get(self, request, *args, **kwargs):

        user = request.user
        user_all_objects = Wallet.objects.filter(user=user)

        queryset =user_all_objects.order_by('-data')
        queryset = self.apply_filters(request, queryset)

        paginator = CustomPageNumberPagination()
        record_list = paginator.paginate_queryset(queryset, request)

        serializer = WalletSerializer(record_list, many=True)

        aggregation_data = user_all_objects.aggregate(
            total_price=Sum('income_or_expence')
        )
        total = aggregation_data['total_price']

        if total is None:
            total = 0

        additional_data = {
            'total': total,
        }

        paginate_response = paginator.get_paginated_response(serializer.data)
        response_data = {**paginate_response.data, **additional_data}

        return Response(response_data)


class AnonymusList(APIView):
    permission_classes = []
    authentication_classes = []

    pagination_class = CustomPageNumberPagination

    def apply_filters(self, request, queryset):
        """Применяем фильтры вручную."""
        filter_backend = DjangoFilterBackend()
        # Применяем фильтрацию с помощью filterset_class
        return filter_backend.filter_queryset(request, queryset, self)

    def get(self, request, *args, **kwargs):
        delete_anonymous_records_after_10_minutes()
        # Берем последние 10
        username = 'worker'
        worker = User.objects.get(username=username)
        queryset = Wallet.objects.filter(Q(user=worker) | Q(user__isnull=True)).order_by('-data')

        queryset = self.apply_filters(request, queryset)
        paginator = CustomPageNumberPagination()
        record_list = paginator.paginate_queryset(queryset, request)
        serializer = WalletSerializer(record_list, many=True)
        # Вычисляем тотал
        aggregation_data = Wallet.objects.filter(Q(user=worker) | Q(user__isnull=True)).aggregate(
            total_price=Sum('income_or_expence')
        )
        total = aggregation_data['total_price']

        if total is None:
            total = 0

        additional_data = {
            'total': total,
        }

        paginate_response = paginator.get_paginated_response(serializer.data)
        response_data = {**paginate_response.data, **additional_data}

        return Response(response_data)


def index(request):
    return render(request, 'index.html', {'user': request.user})


def delete_anonymous_records_after_10_minutes():
    records_to_delete = Wallet.objects.filter(user__isnull=True).values_list('id', flat=True)
    if records_to_delete.exists():
        eta = timezone.now() + timedelta(seconds=300)
        result = delete_anonymous_records.apply_async(args=[list(records_to_delete)], eta=eta)
