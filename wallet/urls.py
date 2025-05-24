from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

default_router = DefaultRouter()
default_router.register(r'wallet', views.GeneralActionsList, basename='wallet'),
default_router.register(r'anonymous_wallet', views.AnonymousListBAsicActions, basename='_anonymous_wallet')

urlpatterns = [
    path('', views.index, name='index'),  # Рендерим HTML-страницу
    path('', include(default_router.urls)),  # API
    # path('home/', views.HomeView.as_view()),
    # path('total/', views.WalletSumView.as_view()),
    path('wallet_record_list/', views.WalletList.as_view()),
    path('anonymous_record_list/', views.AnonymousList.as_view())
]




# from django.urls import path
# from . import views
# from rest_framework.routers import DefaultRouter
#
# #
# # router = DefaultRouter()
# # router.register('wallet/', ActionsList)
#
# urlpatterns = [
#     path('', views.index, name='index'),  # Рендерим HTML-страницу
#     path('api/wallet/', views.ActionsList.as_view(), name='wallet-list-create'),  # API
# ]
# # urlpatterns = [
# #     path('wallet/', ActionsList.as_view(), name='actions-list'),
# # ]