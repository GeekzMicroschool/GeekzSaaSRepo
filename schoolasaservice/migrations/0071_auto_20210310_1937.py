# Generated by Django 3.0.8 on 2021-03-10 14:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolasaservice', '0070_auto_20210310_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrolledstudents',
            name='invoice_show',
            field=models.CharField(default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='inquirys',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 10, 19, 36, 19, 523335)),
        ),
    ]
