# Generated by Django 3.0.8 on 2021-03-03 03:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolasaservice', '0057_auto_20210302_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentapplication',
            name='Enrolled',
            field=models.CharField(default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='inquirys',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 3, 9, 4, 39, 230307)),
        ),
    ]
