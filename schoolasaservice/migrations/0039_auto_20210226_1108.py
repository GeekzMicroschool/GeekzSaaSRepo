# Generated by Django 3.0.8 on 2021-02-26 05:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolasaservice', '0038_auto_20210225_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inquirys',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 2, 26, 11, 7, 17, 507826)),
        ),
    ]
