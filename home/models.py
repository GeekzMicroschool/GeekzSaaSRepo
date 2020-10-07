from django.db import models

# Create your models here.
class UserDetails(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    fullname = models.CharField(max_length=200)
    phone_no = models.BigIntegerField()
    whatsapp_no = models.BigIntegerField(blank=True, null=True)

