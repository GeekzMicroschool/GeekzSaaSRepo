# Generated by Django 3.0.8 on 2021-03-02 10:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolasaservice', '0055_auto_20210302_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inquirys',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 2, 16, 8, 18, 423723)),
        ),
    ]
