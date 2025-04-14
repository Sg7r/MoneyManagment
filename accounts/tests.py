from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework_simplejwt.authentication import JWTAuthentication


# from django.test import TestCase


class TestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='username',
            password='password',
            email='email@gmail.com'
        )
        self.login_url = reverse('login')

        response = self.client.get(self.login_url)  # Укажите свой путь для страницы с CSRF
        # Проверяем, что CSRF-токен присутствует
        self.assertContains(response, 'csrfmiddlewaretoken')
        # Получаем CSRF-токен из cookies
        self.CSRF_token = response.cookies['csrftoken'].value

    def test_csrf_token_in_headers(self):
        response = self.client.post(reverse('login'), {
            'username': self.user.username,
            'password': self.user.password
        }, HTTP_X_CSRFTOKEN=self.CSRF_token)

        # Проверяем, что статус ответа — успешный
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_user(self):

        user = User.objects.filter(username=self.user.username).first()
        if  user:
            self.test_delete_user()

        response = self.client.post(reverse('user-register'), {
            'username': self.user.username,
            'password': self.user.password,
            'email': self.user.email
        }, HTTP_X_CSRFTOKEN=self.CSRF_token)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_user(self):

        user = User.objects.filter(username=self.user.username).first()
        if not user:
            self.test_register_user()
        user = User.objects.get(username=f'{self.user.username}')
        pk = user.pk

        url = reverse('user-delete', kwargs={'pk': pk})
        response = self.client.delete(url, HTTP_X_CSRFTOKEN=self.CSRF_token)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_login(self):

        self.test_register_user()
        url = reverse('login')

        response = self.client.post(url,
        {
            'username': self.user.username,
            'password': self.user.password
        }, HTTP_X_CSRFTOKEN=self.CSRF_token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


