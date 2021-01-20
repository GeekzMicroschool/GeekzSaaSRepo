# Generated by Django 3.0.8 on 2021-01-19 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolasaservice', '0009_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='INDIVIDUAL_WEBPAGE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SCHOOL_NAME', models.CharField(max_length=250)),
                ('LOCALITY', models.CharField(max_length=250)),
                ('AMENITIES', models.CharField(max_length=800)),
                ('BANNER1', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('BANNER2', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('BANNER3', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('BANNER4', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('GOOGLE_REVIEWS_LINK', models.URLField(max_length=300)),
                ('FOUNDER_NAME', models.CharField(max_length=250)),
                ('DESIGNATION', models.CharField(max_length=250)),
                ('CO_FOUNDER1', models.CharField(max_length=250)),
                ('DESIGNATION_CO1', models.CharField(max_length=250)),
                ('CO_FOUNDER2', models.CharField(max_length=250)),
                ('DESIGNATION_CO2', models.CharField(max_length=250)),
                ('CONTENT1', models.CharField(max_length=1000)),
                ('CONTENT2', models.CharField(max_length=1000)),
                ('CONTENT3', models.CharField(max_length=1000)),
                ('ADDRESS1', models.CharField(max_length=400)),
                ('ADDRESS2', models.CharField(max_length=400)),
                ('SCHOOL_LOCALITY', models.CharField(max_length=400)),
                ('SCHOOL_PHONE', models.BigIntegerField()),
                ('SCHOOL_PHONE1', models.BigIntegerField()),
                ('SCHOOL_EMAIL', models.EmailField(max_length=254)),
                ('SCHOOL_HOURS_KS', models.CharField(max_length=250)),
                ('SCHOOL_HOURS_ES', models.CharField(max_length=250)),
            ],
        ),
    ]
