# Generated by Django 3.0.8 on 2021-02-26 10:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolasaservice', '0043_auto_20210226_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inquirys',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 2, 26, 16, 2, 29, 702607)),
        ),
    ]
