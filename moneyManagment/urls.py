from django.contrib import admin
from django.urls import path, include
from wallet.views import ActionsList
from monthly_bills.views import MonthlyBillsList
from rest_framework.routers import DefaultRouter


default_router = DefaultRouter()
default_router.register('api/wallet', ActionsList, 'actions_list')
default_router.register('api/monthly_bills',MonthlyBillsList, 'monthly_bills_list')

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include(default_router.urls))
] + default_router.urls
