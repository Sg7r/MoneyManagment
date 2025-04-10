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

    def get(self, request):
        # if request.method == 'GET':
        return render(request, 'registration.html', {'type': 'register'})

    def post(self, request):
        if request.method == 'POST':
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                data_dict = request.data
                if 'username' in data_dict and 'password' in data_dict and 'email' in data_dict:
                    user = serializer.save()
                    send_confirmation_email.apply_async(
                        kwargs={
                            'username': data_dict['username'],
                            'password': data_dict['password'],
                            'email': data_dict['email']
                        }
                    )

                    return Response({"message": "Registration successful"},
                                    status=status.HTTP_201_CREATED)
                else:
                    print("Missing required fields: username, password, or email")


                # token = Token.objects.create(user=user)
                # return Response({"token": token.key, "message": "Registration successful"},
                #                 status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDeleteView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def delete(self, request, pk):

        user = User.objects.get(id=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) \




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
