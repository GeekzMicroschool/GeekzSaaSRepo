# Generated by Django 3.0.8 on 2021-03-05 13:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolasaservice', '0059_auto_20210304_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inquirys',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 5, 18, 56, 7, 937376)),
        ),
        migrations.AlterUniqueTogether(
            name='individual_admin_slots',
            unique_together={('slot', 'day')},
        ),
    ]
