# Generated by Django 5.1.4 on 2024-12-23 16:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0003_alter_wallet_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 23, 10, 9, 16, 115602)),
        ),
    ]
