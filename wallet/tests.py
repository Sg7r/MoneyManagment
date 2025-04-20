from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from wallet.factories import UserFactory, WalletRecordsFactory
from django.contrib.auth.models import User
from rest_framework import status
from wallet.models import Wallet


def get_jwt_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

def get_anonymous_record_id(json_list):
    for each in json_list:
        if each['user'] is None:
            record_id_anonymus = each['id']
            print("ORIGINAL  response:", each)
            return record_id_anonymus


class TestCase(APITestCase):

    def setUp(self):
        self.login_url = reverse('login')
        self.register_url = reverse('user-register')

        response = self.client.get(self.login_url)  # Укажите свой путь для страницы с CSRF
        self.CSRF_token = response.cookies['csrftoken'].value

        self.user_test = UserFactory()
        user = User.objects.filter(username=self.user_test.username).first()
        if not user:
            self.client.post(reverse('user-register'), {
                'username': self.user_test.username,
                'password': 'password',
                'email': self.user_test.email
            }, HTTP_X_CSRFTOKEN=self.CSRF_token)

        self.access_token = get_jwt_token_for_user(user)
        self.client.cookies['access_token'] = self.access_token

        for i in range(5):
            self.user_test = UserFactory()
            self.wallet_record = WalletRecordsFactory(user=self.user_test)

            user = User.objects.filter(username=self.user_test.username).first()
            if not user:
                self.client.post(reverse('user-register'), {
                    'username': self.user_test.username,
                    'password': 'password',
                    'email': self.user_test.email
                }, HTTP_X_CSRFTOKEN=self.CSRF_token)

            if i % 2 == 0:
                self.client.post('/api/anonymous_wallet/', {
                    'income_or_expence': self.wallet_record.income_or_expence,
                    'target': self.wallet_record.target,
                    'data': self.wallet_record.data,
                }, HTTP_X_CSRFTOKEN=self.CSRF_token)
            else:
                self.client.post('/api/wallet/', {
                    'income_or_expence': self.wallet_record.income_or_expence,
                    'target': self.wallet_record.target,
                    'data': self.wallet_record.data,
                    'user': self.wallet_record.user.id
                }, HTTP_X_CSRFTOKEN=self.CSRF_token)

    def test_create_record_logged_user(self):
        response = self.client.post('/api/wallet/', {
            'income_or_expence': self.wallet_record.income_or_expence,
            'target': self.wallet_record.target,
            'data': self.wallet_record.data,
            'user': self.wallet_record.user.id
        }, HTTP_X_CSRFTOKEN=self.CSRF_token)

        print("POST response:", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_change_record_logged_user(self):
        url = '/api/wallet/' + str(self.wallet_record.id) + '/'

        response = self.client.patch(url, {
            'income_or_expence': self.wallet_record.income_or_expence,
            'target': 'changed',
        }, HTTP_X_CSRFTOKEN=self.CSRF_token)

        print("PATCH response:", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_record_logged_user(self):
        url = '/api/wallet/' + str(self.wallet_record.id) + '/'
        print("URL for handling", url)

        response = self.client.delete(url, {
            'income_or_expence': self.wallet_record.income_or_expence,
            'target': 'changed',
            'data': 'changed',
            'user': 'changed'
        }, HTTP_X_CSRFTOKEN=self.CSRF_token)

        print("Delete response:", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_record_anonymous_user(self):
        self.access_token = None

        response = self.client.post('/api/anonymous_wallet/', {
            'income_or_expence': self.wallet_record.income_or_expence,
            'target': self.wallet_record.target,
            'data': self.wallet_record.data,
        }, HTTP_X_CSRFTOKEN=self.CSRF_token)

        print("POST response:", response.status_code, response.data)
        self.assertEqual(response.data["user"], None)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_change_record_anonymous_user(self):
        self.access_token = None

        response = self.client.get('/api/anonymous_wallet/', HTTP_X_CSRFTOKEN=self.CSRF_token)
        all_records = response.json()
        record_id = get_anonymous_record_id(all_records)

        url = '/api/anonymous_wallet/' + str(record_id) + '/'
        response = self.client.patch(url, {
            'target': 'changed',
        }, HTTP_X_CSRFTOKEN=self.CSRF_token)

        print("PATCH response:", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_record_anonymous_user(self):
        self.access_token = None

        response = self.client.get('/api/anonymous_wallet/', HTTP_X_CSRFTOKEN=self.CSRF_token)
        all_records = response.json()
        record_id = get_anonymous_record_id(all_records)

        url = '/api/anonymous_wallet/' + str(record_id) + '/'
        response = self.client.delete(url, HTTP_X_CSRFTOKEN=self.CSRF_token)

        print("Delete response:", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
