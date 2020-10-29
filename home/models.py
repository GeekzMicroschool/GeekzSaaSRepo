from django.db import models

# Create your models here.
class USER_DETAILS(models.Model):
   uid=models.CharField(max_length=50, primary_key=True)
   FULL_NAME=models.CharField(max_length=100)
   USER_EMAIL=models.EmailField(max_length=254, unique=True)
   CONTACT_PHONE=models.BigIntegerField()
   PHONE_CTRY_CODE=models.IntegerField()
   WHATSAPP_FLAG=models.CharField(max_length=1, default="N")
   AUTH_TYPE=models.IntegerField()
   IS_PARENT=models.CharField(max_length=1, default="N")
   IS_STUDENT=models.CharField(max_length=1, default="N")
   IS_MICROSCHOOL=models.CharField(max_length=1, default="N")
   IS_QUESTSCHOOL=models.CharField(max_length=1, default="N")
   IS_HOMESCHOOL=models.CharField(max_length=1, default="N")
   PHOTO_URL=models.URLField(max_length=300)