from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Извлекаем JWT токен из куки
        token = request.COOKIES.get('access_token')

        if not token:
            raise AuthenticationFailed('No JWT token in cookies')

        try:
            # Декодируем и проверяем токен
            validated_token = self.get_validated_token(token)
        except Exception as e:
            raise AuthenticationFailed('Invalid token')

        return self.get_user(validated_token), validated_token