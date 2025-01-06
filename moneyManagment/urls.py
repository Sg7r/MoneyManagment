from django.contrib import admin
from django.urls import path, include
from wallet.views import ActionsList
from monthly_bills.views import MonthlyBillsList
from accounts.views import RegisterView
# from accounts.views import CreateUserView
from rest_framework.routers import DefaultRouter


default_router = DefaultRouter()
# default_router.register('api/wallet', ActionsList, 'actions_list')
default_router.register('api/monthly_bills', MonthlyBillsList, 'monthly_bills_list')
# default_router.register('api/register', CreateUserView, 'Create_UserView')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('wallet.urls')),  # Подключаем HTML-страницу
    # path('api/', include('accounts.urls')),
    path('api/users/', include('accounts.urls')),  # Подключаем HTML-страницу
    # path('login/', index, name='index'),  # Рендерим login - HTML-страницу



    # path('api/wallet', include('wallet.urls')) # Подключаем API
] + default_router.urls
