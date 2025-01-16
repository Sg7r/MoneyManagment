from django.shortcuts import render, redirect
from rest_framework.views import APIView
from .models import Wallet
from .serializer import WalletSerializer, SumResponseSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from django.db.models import Sum, Avg
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import CustomPageNumberPagination


class ActionsList(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    # pagination_class = CustomPageNumberPagination
    # filter_backends = (DjangoFilterBackend,)  # Указываем фильтрацию
    # filterset_class = ProductFilter # Указываем класс фильтра

    # def list(self, request, *args, **kwargs):
    #     """
    #     Переопределение метода list для обработки GET-запроса.
    #     """
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     for each in serializer.data:
    #
    #     breakpoint()
    #
    #     return Response(serializer.data)


# class HomeView(APIView):
#     authentication_classes = [JWTAuthentication]  # Аутентификация через JWT
#     permission_classes = []  # Нет ограничений для публичного доступа
#
#     def get(self, request):
#         if request.user.is_authenticated:
#             # Если пользователь аутентифицирован, перенаправляем на страницу с API или редирект
#             return redirect('index')
#         else:
#             # Если пользователь не аутентифицирован, рендерим базовую страницу
#             # return render(request, 'home.html')  # Ваш HTML-шаблон для неаутентифицированных пользователей
#             return redirect('index', {'user': ''})

class WalletShortList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Берем последние 10>\
        user = request.user
        # username = user.username
        short_list = Wallet.objects.filter(user=user).order_by('-data')[:10]
        serializer = WalletSerializer(short_list, many=True)
        # Возвращаем результат через сериализатор
        return Response(serializer.data, status=status.HTTP_200_OK)


class WalletSumView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        # Агрегируем данные и получаем сумму
        aggregation_data = Wallet.objects.filter(user=user).aggregate(
            total_price=Sum('income_or_expence')
        )
        total = aggregation_data['total_price']

        # Если сумма равна None (если продуктов нет), то ставим 0
        if total is None:
            total = 0

        # Возвращаем результат через сериализатор
        return Response(SumResponseSerializer({'total_price': total}).data)


def index(request):
    return render(request, 'index.html', {'user': request.user})
