# Generated by Django 3.0.8 on 2021-02-16 13:46

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django_imgur.storage
import schoolasaservice.models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolasaservice', '0023_auto_20210209_1029'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo_webpage1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('file', models.FileField(blank=True, null=True, storage=django_imgur.storage.ImgurStorage(), upload_to=schoolasaservice.models.user_directory_path_gala)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('gala_admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolasaservice.INDIVIDUAL_WEBPAGESS1')),
            ],
        ),
        migrations.AlterField(
            model_name='inquiry',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 2, 16, 19, 16, 36, 845786)),
        ),
        migrations.DeleteModel(
            name='Photo_webpage',
        ),
    ]
