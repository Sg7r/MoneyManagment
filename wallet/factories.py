import factory
from faker import Faker
import factory.fuzzy
from factory.django import DjangoModelFactory
from wallet.models import Wallet
from django.contrib.auth.models import User
from django.db import models

faker = Faker()
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.LazyAttribute(lambda x: faker.user_name())
    email = 'email@gmail.com'
    password = factory.PostGenerationMethodCall('set_password', 'password')


class WalletRecordsFactory(DjangoModelFactory):
    class Meta:
        model = Wallet

    user = factory.SubFactory(UserFactory)
    income_or_expence = factory.fuzzy.FuzzyInteger(-999, 999)
    target = factory.Faker('sentence', nb_words=5)
    data = factory.Faker('date_time_this_month')



