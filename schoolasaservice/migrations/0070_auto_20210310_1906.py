# Generated by Django 3.0.8 on 2021-03-10 13:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolasaservice', '0069_auto_20210308_2212'),
    ]

    operations = [
        migrations.AddField(
            model_name='individual_webpagess1',
            name='invoice_generation',
            field=models.CharField(default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='inquirys',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 10, 19, 5, 18, 779637)),
        ),
    ]
