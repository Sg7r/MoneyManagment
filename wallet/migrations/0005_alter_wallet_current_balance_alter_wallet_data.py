# Generated by Django 5.1.4 on 2024-12-30 04:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0004_alter_wallet_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='current_balance',
            field=models.SmallIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 29, 22, 26, 44, 128752)),
        ),
    ]
