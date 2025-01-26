import django_filters
from .models import Wallet

from rest_framework import viewsets
from .serializer import WalletSerializer


class WalletFilter(django_filters.FilterSet):
    low_range = django_filters.NumberFilter(field_name='income_or_expence',  lookup_expr='gte')
    max_range = django_filters.NumberFilter(field_name='income_or_expence', lookup_expr='lte')
    target = django_filters.CharFilter(field_name='target', lookup_expr='icontains')


    class Meta:
        model = Wallet
        fields = ['income_or_expence', 'target']  # поля, по которым будет доступна фильтрация
