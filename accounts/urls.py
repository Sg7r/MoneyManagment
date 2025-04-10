from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='user-register'),
    path('register/<int:pk>/', views.UserDeleteView.as_view(), name='user-delete'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('login_page/', views.LoginViewPage, name='login'),


]
