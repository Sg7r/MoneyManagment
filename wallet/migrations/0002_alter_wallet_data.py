# Generated by Django 5.1.4 on 2024-12-23 15:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='data',
            field=models.DateField(default=datetime.datetime(2024, 12, 23, 9, 12, 4, 879147)),
        ),
    ]
