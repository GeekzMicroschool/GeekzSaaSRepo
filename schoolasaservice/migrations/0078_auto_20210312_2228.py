# Generated by Django 3.0.8 on 2021-03-12 16:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolasaservice', '0077_auto_20210312_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inquirys',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 12, 22, 28, 16, 652272)),
        ),
    ]
