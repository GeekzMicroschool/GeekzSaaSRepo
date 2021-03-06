from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from home.models import USER_DETAILS
import sys
from PIL import Image
from io import BytesIO
from datetime import datetime  
from django.core.files.uploadedfile import InMemoryUploadedFile
from django_imgur.storage import ImgurStorage 


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
    slot = models.CharField(max_length=200)
    day = models.CharField(max_length=200) 
    duration = models.CharField(max_length=200)
    class Meta:
        unique_together = ('admin','slot','day',)


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

class MICRO_PROFILIN(models.Model):
    uid=models.CharField(max_length=50, primary_key=True)
    IS_PROFILINGCOMPLETE=models.CharField(max_length=1, default="N")
    slot = models.ForeignKey(SLOTS_DAY, on_delete=models.CASCADE)
    schedule_date = models.DateField()
    USER = models.CharField(max_length=250)
    EVENT_ID = models.CharField(max_length=600)
    ICalUID = models.CharField(max_length=600)
    hangoutLink = models.CharField(max_length=600)
    START_TIME = models.CharField(max_length=250)
    END_TIME = models.CharField(max_length=250)
    HEADING = models.CharField(max_length=300)

class MICRO_PROFILING(models.Model):
    uid=models.CharField(max_length=50, primary_key=True)
    IS_PROFILINGCOMPLETE=models.CharField(max_length=1, default="N")
    IS_APPROVED=models.CharField(max_length=1, default="N")
    slot = models.ForeignKey(SLOTS_DAY, on_delete=models.CASCADE)
    schedule_date = models.DateField()
    USER = models.CharField(max_length=250)
    EVENT_ID = models.CharField(max_length=600)
    ICalUID = models.CharField(max_length=600)
    hangoutLink = models.CharField(max_length=600)
    START_TIME = models.CharField(max_length=250)
    END_TIME = models.CharField(max_length=250)
    HEADING = models.CharField(max_length=300)    

class RESCHEDULE_REASON(models.Model):
    uid =  models.CharField(max_length=50, primary_key=True)
    reason = models.CharField(max_length=10000)  



STORAGE = ImgurStorage()
# the storage  calls the storage function in imgurpython present in env/src/imgurpython

'''def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename) '''   

def content_file_name(instance,filename):
    return '/'.join(['uploads','banner1',filename])

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'microschool_{0}/{1}'.format(instance.SCHOOL_NAME , filename)    

class INDIVIDUAL_WEBPAGESS1(models.Model):
    uid = models.CharField(max_length=50, primary_key=True)
    SCHOOL_NAME = models.CharField(max_length=250)   
    LOCALITY = models.CharField(max_length=250) 
    AMENITIES_is_Spacious_Studio = models.CharField(max_length=1, default="N")
    AMENITIES_is_Outdoor_PlayLawn = models.CharField(max_length=1, default="N")
    AMENITIES_is_Commute = models.CharField(max_length=1, default="N")
    AMENITIES_is_WiFi = models.CharField(max_length=1, default="N")
    AMENITIES_is_CCTV = models.CharField(max_length=1, default="N")
    AMENITIES_is_Device = models.CharField(max_length=1, default="N")
    AMENITIES_is_Food = models.CharField(max_length=1, default="N")
    AMENITIES_is_Daycare = models.CharField(max_length=1, default="N")
    AMENITIES_is_After_School = models.CharField(max_length=1, default="N")
    AMENITIES_is_Residential = models.CharField(max_length=1, default="N")
    BANNER1 = models.ImageField(upload_to='geekz', storage=STORAGE, null=True, blank=True)
    BANNER2 = models.ImageField(upload_to='geekz', storage=STORAGE, null=True, blank=True)
    BANNER3 =  models.ImageField(upload_to='geekz', storage=STORAGE, null=True, blank=True)
    BANNER4 = models.ImageField(upload_to='geekz', storage=STORAGE, null=True, blank=True)
    GOOGLE_REVIEWS_LINK = models.URLField(max_length=300)
    FOUNDER_NAME = models.CharField(max_length=250) 
    DESIGNATION = models.CharField(max_length=250) 
    CO_FOUNDER1 = models.CharField(max_length=250) 
    DESIGNATION_CO1 = models.CharField(max_length=250) 
    CO_FOUNDER2 = models.CharField(max_length=250) 
    DESIGNATION_CO2 = models.CharField(max_length=250) 
    CONTENT1 = models.CharField(max_length=1000) 
    CONTENT2 = models.CharField(max_length=1000)
    CONTENT3 = models.CharField(max_length=1000)
    ADDRESS1 = models.CharField(max_length=400)
    ADDRESS2 = models.CharField(max_length=400)
    SCHOOL_LOCALITY = models.CharField(max_length=400)
    SCHOOL_PHONE = models.BigIntegerField()
    SCHOOL_PHONE1 = models.BigIntegerField()
    SCHOOL_EMAIL = models.EmailField(max_length=254)
    SCHOOL_HOURS_KS = models.CharField(max_length=250) 
    SCHOOL_HOURS_ES = models.CharField(max_length=250) 
    IS_COMPLETE = models.CharField(max_length=1, default="N")
    IS_APPROVED = models.CharField(max_length=1, default="N")
    LATITUDE = models.FloatField(max_length=600)
    LONGITUDE = models.FloatField(max_length=600)

    '''def save(self, *args, **kwargs):
        if not self.uid:
            self.BANNER1 = self.compressImage(self.BANNER1)
        super(INDIVIDUAL_WEBPAGESS, self).save(*args, **kwargs)
    
    def compressImage(self,BANNER1):
        print(BANNER1) 
        imageTemproary = Image.open(BANNER1)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize( (1020,573) ) 
        imageTemproary.save(outputIoStream , format='JPEG', quality=60)
        outputIoStream.seek(0)
        BANNER1 = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % BANNER1.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return BANNER1 '''


class feedback_user(models.Model):
    name = models.CharField(max_length=250)  
    feedback = models.CharField(max_length=700) 
    rating = models.IntegerField()
    user_id = models.CharField(max_length=100)
    SCHOOL = models.CharField(max_length=100)
    school_name = models.ForeignKey(INDIVIDUAL_WEBPAGESS1, on_delete=models.CASCADE)


class notify_users(models.Model):
    email = models.CharField(max_length=300)
    phone = models.BigIntegerField()

class Country(models.Model):
    name = models.CharField(max_length=30)

class City(models.Model):
    name = models.CharField(max_length=30)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    population = models.PositiveIntegerField()    

class InquiryS(models.Model):
    uid = models.CharField(max_length=50, primary_key=True)
    date = models.DateTimeField(default=datetime.now(), blank=True)
    studentName = models.CharField(max_length=250)
    enrolling_grade = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    phone = models.BigIntegerField()
    ISAPPROVED = models.CharField(max_length=1, default="N")
    hear_about_us = models.CharField(max_length=250) 
    microschool = models.CharField(max_length=250) 

def user_directory_path_gala(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'micro_{0}{1}'.format(instance.gala_admin.SCHOOL_NAME , filename)   

class individual_feedetail(models.Model):
    admin = models.ForeignKey(INDIVIDUAL_WEBPAGESS1, on_delete=models.CASCADE)
    fullYear_kindergarten = models.IntegerField()
    fall_kindergarten= models.IntegerField()
    spring_kindergarten =  models.IntegerField()
    fullYear_lowerElementary = models.IntegerField()
    fall_lowerElementary = models.IntegerField()
    spring_lowerElementary =  models.IntegerField()
    fullYear_UpperElementary = models.IntegerField()
    fall_UpperElementary = models.IntegerField()
    spring_UpperElementary =  models.IntegerField()

class Photo_webpage1(models.Model):
    title = models.CharField(max_length=255, blank=True)
    gala_admin = models.ForeignKey(INDIVIDUAL_WEBPAGESS1, on_delete=models.CASCADE)
    file = models.ImageField(upload_to='geekz', storage=STORAGE, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

##https://geekzmicroschoolgallery.imgur.com/all/  the link to imgur api  


class studentApplication(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    gender = models.CharField(max_length=250)
    SaaSDOB = models.DateField()
    enrolling_year = models.CharField(max_length=250)
    enrolling_grade = models.CharField(max_length=250)
    attendedschool = models.CharField(max_length=250)
    Fathersname = models.CharField(max_length=250)
    Fathersoccupation = models.CharField(max_length=250)
    Mothersname = models.CharField(max_length=250)
    Mothersoccupation = models.CharField(max_length=250)
    income = models.CharField(max_length=250)
    address = models.CharField(max_length=800)
    email = models.EmailField(max_length=250)
    phone = models.BigIntegerField()
    geekzcommute = models.CharField(max_length=250)
    yescommutelocation = models.CharField(max_length=250)
    childproud = models.CharField(max_length=800)
    familyactivities = models.CharField(max_length=800)
    childsinterests = models.CharField(max_length=800)
    yourdreams = models.CharField(max_length=800)
    medicalcondition = models.CharField(max_length=800)
    childsuspended = models.CharField(max_length=800)
    anythingelse = models.CharField(max_length=800)
    hear_about = models.CharField(max_length=100)
    IS_COMPLETE= models.CharField(max_length=1, default="N")
    microschool = models.ForeignKey(INDIVIDUAL_WEBPAGESS1, on_delete=models.CASCADE)
    status = models.CharField(max_length=250)
    student_id = models.CharField(max_length=100,primary_key=True)
    Profiling_scheduled = models.CharField(max_length=1, default="N")
    Profiling_complete = models.CharField(max_length=1, default="N")
    Profiling_approved = models.CharField(max_length=1, default="N")
    Enrolled = models.CharField(max_length=1, default="N")

class Individual_admin_slots(models.Model):
    admin_id = models.ForeignKey(INDIVIDUAL_WEBPAGESS1, on_delete=models.CASCADE)
    slot = models.TextField()
    day = models.TextField() 
    duration = models.TextField()
    class Meta:
        unique_together = ('admin_id','slot','day',)

class StudentProfiling(models.Model):
    uid=models.ForeignKey(studentApplication, on_delete=models.CASCADE)
    IS_PROFILINGCOMPLETE=models.CharField(max_length=1, default="N")
    IS_APPROVED=models.CharField(max_length=1, default="N")
    slot = models.ForeignKey(Individual_admin_slots, on_delete=models.CASCADE)
    schedule_date = models.DateField()
    USER = models.CharField(max_length=250)
    EVENT_ID = models.CharField(max_length=600)
    ICalUID = models.CharField(max_length=600)
    hangoutLink = models.CharField(max_length=600)
    START_TIME = models.CharField(max_length=250)
    END_TIME = models.CharField(max_length=250)
    HEADING = models.CharField(max_length=300)  
    modeofprofiling =  models.CharField(max_length=300) 

class InvoiceRequest(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    Fathersname = models.CharField(max_length=250)
    address = models.CharField(max_length=800)
    email = models.EmailField(max_length=250)
    microschool = models.CharField(max_length=800)
    student_id = models.CharField(max_length=100)
    IS_COMPLETE= models.CharField(max_length=1, default="N")



class transcriptsRequest(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    Fathersname = models.CharField(max_length=250)
    address = models.CharField(max_length=800)
    email = models.EmailField(max_length=250)
    microschool = models.CharField(max_length=800)
    student_id = models.CharField(max_length=100)
    payment_complete = models.CharField(max_length=1, default="N")
    IS_COMPLETE= models.CharField(max_length=1, default="N")

class enrolledStudents(models.Model):
    student_enrolled = models.ForeignKey(studentApplication, on_delete=models.CASCADE)
    active_status = models.CharField(max_length=1, default="N")
    fees_paid  =   models.CharField(max_length=1, default="N")
    

    












     

######################################################################################3

