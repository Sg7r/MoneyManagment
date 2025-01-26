from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
import datetime
from .tasks import send_confirmation_email


class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    # def send_conf_email(self, data_dict):
    #     print(send_confirmation_email.delay())
    #     return Response()

    def get(self, request):
        if request.method == 'GET':
            return render(request, 'registration.html', {'type': 'register'})

    def post(self, request):
        if request.method == 'POST':
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()

                data_dict = request.data
                if 'username' in data_dict and 'password' in data_dict and 'email' in data_dict:
                    send_confirmation_email.apply_async(
                        kwargs={
                            'username': data_dict['username'],
                            'password': data_dict['password'],
                            'email': data_dict['email']
                        }
                    )
                    # send_confirmation_email(
                    #         data_dict['username'],
                    #         data_dict['password'],
                    #         data_dict['email']
                    # )
                else:
                    print("Missing required fields: username, password, or email")


                token = Token.objects.create(user=user)
                return Response({"token": token.key, "message": "Registration successful"},
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(
    #     detatil=True,
    #     methods=['POST'],
    # )



class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):

                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                # Save token to Cookies
                response = JsonResponse({"message": "Login successful"}, status=status.HTTP_200_OK)
                response.set_cookie(
                    key='access_token',
                    value=access_token,
                    httponly=False,  # Только для серверных запросов, не доступно через JS
                    max_age=datetime.timedelta(minutes=5),  # Время жизни токена
                    samesite='Strict',  # Защищает от CSRF атак
                )
                response.set_cookie(
                    key='refresh_token',
                    value=refresh_token,
                    httponly=True,
                    max_age=datetime.timedelta(days=1),  # Время жизни refresh токена
                    samesite='Strict',
                )
                # return Response({"token": token.key}, status=status.HTTP_200_OK)
                return response
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


def LoginViewPage(request):
    return render(request, 'accounts.html', {'type': 'login'})
