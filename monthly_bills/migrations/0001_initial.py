# Generated by Django 5.1.4 on 2024-12-23 16:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyBills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_name', models.TextField()),
                ('rate', models.SmallIntegerField()),
                ('date_to_pay', models.DateTimeField(default=datetime.datetime(2024, 12, 23, 10, 9, 16, 115602))),
                ('paid', models.BooleanField()),
            ],
        ),
    ]
