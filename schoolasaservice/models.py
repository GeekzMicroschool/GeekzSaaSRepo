from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from home.models import USER_DETAILS
<<<<<<< HEAD
import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
=======
>>>>>>> 73dff70a9d2f7665f71dff4e6c98f9e913ccc8f7

# Create your models here.
class MICRO_APPLN(models.Model):
    uid=models.CharField(max_length=50, primary_key=True)
    IS_COMPLETE=models.CharField(max_length=1, default="N")
    NAME=models.CharField(max_length=100)
    DOB=models.DateField()
    EMAIL=models.EmailField(max_length=254)
    COUNTRY_CODE=models.IntegerField()
    PHONE=models.BigIntegerField()
    LOVE_TO_BE=models.CharField(max_length=15)
    SCHOOL_MODE=models.CharField(max_length=25)
    SCHOOL_OPERATE=models.CharField(max_length=25)
    SCHOOL_AREA=models.CharField(max_length=100)
    SCHOOL_CITY=models.CharField(max_length=100)
    BUSINESS=models.CharField(max_length=50)
    SCHOOL_NAME=models.CharField(max_length=200, blank=True, null=True)
    SCHOOL_WEBSITE=models.CharField(max_length=300, blank=True, null=True)
    SCHOOL_FB=models.URLField(max_length=300, blank=True, null=True)
    LINKEDIN=models.URLField(max_length=300)
    OCCUPATION=models.CharField(max_length=100)
    PASSION=models.CharField(max_length=10000)
    WHY_AFFILIATE=models.CharField(max_length=10000)


class QUEST_APPLN(models.Model):
    uid=models.CharField(max_length=50, primary_key=True)
    IS_COMPLETE=models.CharField(max_length=1, default="N")
    NAME=models.CharField(max_length=100)
    DOB=models.DateField()
    EMAIL=models.EmailField(max_length=254)
    COUNTRY_CODE=models.IntegerField()
    PHONE=models.BigIntegerField()
    LOVE_TO_BE=models.CharField(max_length=15)
    SCHOOL_MODE=models.CharField(max_length=25)
    SCHOOL_OPERATE=models.CharField(max_length=25)
    SCHOOL_AREA=models.CharField(max_length=100)
    SCHOOL_CITY=models.CharField(max_length=100)
    BUSINESS=models.CharField(max_length=50)
    SCHOOL_NAME=models.CharField(max_length=200, blank=True, null=True)
    SCHOOL_WEBSITE=models.CharField(max_length=300, blank=True, null=True)
    SCHOOL_FB=models.URLField(max_length=300, blank=True, null=True)
    LINKEDIN=models.URLField(max_length=300)
    OCCUPATION=models.CharField(max_length=100)
    PASSION=models.CharField(max_length=10000)
    WHY_AFFILIATE=models.CharField(max_length=10000)


class MICRO_AUDN(models.Model):
    uid=models.CharField(max_length=50, primary_key=True)
    IS_COMPLETE=models.CharField(max_length=1, default="N")
    IS_APPROVED=models.CharField(max_length=1, default="N")
    ENGLISH_FLUENCY=models.CharField(max_length=15)
    CODING_SKILL=models.CharField(max_length=15)
    PHOTO_EDITING=models.CharField(max_length=15)
    VIDEO_EDITING=models.CharField(max_length=15)
    PASSION_TO_LEARN=models.CharField(max_length=10)
    FINANCIAL_MONEY_REQUIRED=models.CharField(max_length=10000)
    MONEY_COME_FROM=models.CharField(max_length=300)
    HD_WEBCAM=models.CharField(max_length=5)
    INTERNET_MODE=models.CharField(max_length=20)
    INTERNET_SPEED=models.CharField(max_length=5)
    YOUTUBE_VIDEO=models.URLField(max_length=300)
    NO_OF_STUDENTS=models.IntegerField()
    QUESTIONS=models.CharField(max_length=10000)


class QUEST_AUDN(models.Model):
    uid=models.CharField(max_length=50, primary_key=True)
    IS_COMPLETE=models.CharField(max_length=1, default="N")
    IS_APPROVED=models.CharField(max_length=1, default="N")
    ENGLISH_FLUENCY=models.CharField(max_length=15)
    CODING_SKILL=models.CharField(max_length=15)
    PHOTO_EDITING=models.CharField(max_length=15)
    VIDEO_EDITING=models.CharField(max_length=15)
    PASSION_TO_LEARN=models.CharField(max_length=10)
    HD_WEBCAM=models.CharField(max_length=5)
    INTERNET_MODE=models.CharField(max_length=20)
    INTERNET_SPEED=models.CharField(max_length=5)
    YOUTUBE_VIDEO=models.URLField(max_length=300)
    QUESTIONS=models.CharField(max_length=10000)
    NO_OF_STUDENTS=models.IntegerField()



class MICRO_APPLY(models.Model):
    uid=models.CharField(max_length=50, primary_key=True)
    IS_COMPLETE=models.CharField(max_length=1, default="N")
    NAME=models.CharField(max_length=100)
    DOB=models.DateField()
    EMAIL=models.EmailField(max_length=254)
    COUNTRY_CODE=models.IntegerField()
    PHONE=models.BigIntegerField()
    LOVE_TO_BE=models.CharField(max_length=15)
    SCHOOL_MODE=models.CharField(max_length=25)
    SCHOOL_OPERATE=models.CharField(max_length=25)
    SCHOOL_LOCALITY=models.CharField(max_length=500)
    location = models.PointField(geography=True,default=Point(0.0,0.0))
    BUSINESS=models.CharField(max_length=50)
    SCHOOL_NAME=models.CharField(max_length=200, blank=True, null=True)
    SCHOOL_WEBSITE=models.CharField(max_length=300, blank=True, null=True)
    SCHOOL_FB=models.URLField(max_length=300, blank=True, null=True)
    LINKEDIN=models.URLField(max_length=300)
    OCCUPATION=models.CharField(max_length=100)
    PASSION=models.CharField(max_length=10000)
    WHY_AFFILIATE=models.CharField(max_length=10000)


class SLOTS_DAY(models.Model):
    admin = models.CharField(max_length=200)
    slot = models.TextField()
    day = models.TextField() 
    duration = models.TextField()

class EVENTS_SCHEDULE(models.Model):
    user_details = models.ForeignKey(USER_DETAILS,on_delete=models.CASCADE)
    slot = models.ForeignKey(SLOTS_DAY, on_delete=models.CASCADE)
    summery = models.CharField(max_length=200)
    description =  models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    schedule_date = models.DateField()
    dummy_field = models.CharField(max_length=200)
    class Meta:
        unique_together = ("user_details", "slot","start_time")

<<<<<<< HEAD
######################### auto webpage creation ###########################
class webdata21(models.Model):
    url =  models.CharField(max_length=250,unique=True,blank=False,null=False)
    title = models.CharField(max_length=250,unique=True,blank=False,null=False) 
    Infrastructure_affliation = models.CharField(max_length=250)
    Education_affliation = models.CharField(max_length=250)
    HomeSchool_affliation = models.CharField(max_length=250)
    School_Fee_rule = models.CharField(max_length=250)
    brandFee_rule = models.CharField(max_length=250)
    profile = models.ImageField(upload_to='media/',blank=True , null=True)
    admin_email = models.CharField(max_length=250)
    def save(self, *args, **kwargs):
        if not self.id:
            self.profile = self.compressImage(self.profile)
        super(webdata21, self).save(*args, **kwargs)
    
    def compressImage(self,profile): 
        imageTemproary = Image.open(profile)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize( (1020,573) ) 
        imageTemproary.save(outputIoStream , format='JPEG', quality=60)
        outputIoStream.seek(0)
        profile = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % profile.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return profile

######################################################################################3
=======
>>>>>>> 73dff70a9d2f7665f71dff4e6c98f9e913ccc8f7

