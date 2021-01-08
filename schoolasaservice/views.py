from django.shortcuts import render, redirect
from .models import MICRO_APPLN, QUEST_APPLN, MICRO_AUDN, QUEST_AUDN,MICRO_APPLY
from home.models import USER_DETAILS
from django.contrib.auth.models import User,auth
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
#for sending email
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.gis.geos import Point
###django calendar #####
import calendar
from pytz import timezone
import httplib2
from googleapiclient.discovery import build  #pip install google-api-python-client
from oauth2client.service_account import ServiceAccountCredentials #pip install oauth2client
from .models import *
from .forms import SlotCreationForm
from uuid import uuid4
import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from .decorators import  allowed_users
from django.contrib.auth.models import Group

# Create your views here.
def searchbar(request):
    return render(request,'searchbar.html')
@login_required
def apply(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    fullname=user.first_name+" "+user.last_name
    email=user.email
    if USER_DETAILS.objects.filter(USER_EMAIL=user.email):
        user_detail=USER_DETAILS.objects.get(USER_EMAIL=user.email)
        if user_detail.IS_MICROSCHOOL=="Y" or user_detail.IS_QUESTSCHOOL=="Y":
            #user already submitted the application redirect to audition
            return redirect('audition')
        else:
            return render(request, 'apply.html',{'fullname':fullname, 'email':email})
    else:
        return render(request, 'apply.html',{'fullname':fullname, 'email':email})
        

@login_required
def saasapplication(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    social_data=SocialAccount.objects.get(user_id=user.id)
    
    if request.method == "POST":
        SaaSName=request.POST['SaaSName']
        SaaSDOB=request.POST['SaaSDOB']
        SaaSEmail=request.POST['SaaSEmail']
        SaaSCountryCode=request.POST['SaaSCountryCode']
        SaaSPhone=request.POST['SaaSPhone']
        SaaSLTB=request.POST['SaaSLTB']
        SaaSSchoolMode=request.POST['SaaSSchoolMode']
        SaaSSOperate=request.POST['SaaSSOperate']
        SaaSSchoolArea=request.POST['SaaSSchoolArea']
        SaaSSchoolLatitude=float(request.POST['loc_lat'])
        SaaSSchoolLongitude=float(request.POST['loc_long'])
        #SaaSSchoolCity=request.POST['SaaSSchoolCity']
        SaaSBusiness=(request.POST['SaaSBusiness'])
        SaaSLinkedin=(request.POST['SaaSLinkedin'])
        SaaSOccupation=request.POST['SaaSOccupation']
        SaaSPassion=request.POST['SaaSPassion']
        SaaSWhyAffiliate=request.POST['SaaSWhyAffiliate']
        print(type(SaaSSchoolLatitude))
        print(type(SaaSSchoolLongitude))
        print(SaaSSchoolLatitude)
        print(SaaSSchoolLongitude)
        if SaaSBusiness!="No":
            #other than No value then get following data and store in db
            SaaSSchoolName=request.POST['SaaSSchoolName']
            SaaSSchoolWebsite=request.POST['SaaSSchoolWebsite']
            SaaSSchoolFB=request.POST['SaaSSchoolFB']
            #check whether love to become is microschool or questschool
            if SaaSLTB=="Questschool":
                #store all the data in QUEST_APPLN table
                new_qschool=QUEST_APPLN(
                                uid=social_data.uid,
                                IS_COMPLETE="Y",
                                NAME=SaaSName,
                                DOB=SaaSDOB,
                                EMAIL=SaaSEmail,
                                COUNTRY_CODE=SaaSCountryCode,
                                PHONE=SaaSPhone,
                                LOVE_TO_BE=SaaSLTB,
                                SCHOOL_MODE=SaaSSchoolMode,
                                SCHOOL_OPERATE=SaaSSOperate,
                                SCHOOL_AREA=SaaSSchoolArea,
                                SCHOOL_CITY=SaaSSchoolCity,
                                BUSINESS=SaaSBusiness,
                                SCHOOL_NAME=SaaSSchoolName,
                                SCHOOL_WEBSITE=SaaSSchoolWebsite,
                                SCHOOL_FB=SaaSSchoolFB,
                                LINKEDIN=SaaSLinkedin,
                                OCCUPATION=SaaSOccupation,
                                PASSION=SaaSPassion,
                                WHY_AFFILIATE=SaaSWhyAffiliate
                            )
                new_qschool.save()
                #store some details in USER_DETAILS from the application and social_account
                new_user_details=USER_DETAILS(
                                    uid=social_data.uid,
                                    FULL_NAME=SaaSName,
                                    USER_EMAIL=SaaSEmail,
                                    CONTACT_PHONE=SaaSPhone,
                                    PHONE_CTRY_CODE=SaaSCountryCode,
                                    AUTH_TYPE=1,
                                    IS_QUESTSCHOOL="Y",
                                    PHOTO_URL=social_data.extra_data["picture"]                     
                                )
                new_user_details.save()
            elif SaaSLTB=="Microschool":
                #store all the data in MICRO_APPLN table
                new_mschool=MICRO_APPLY(
                                uid=social_data.uid,
                                IS_COMPLETE="Y",
                                NAME=SaaSName,
                                DOB=SaaSDOB,
                                EMAIL=SaaSEmail,
                                COUNTRY_CODE=SaaSCountryCode,
                                PHONE=SaaSPhone,
                                LOVE_TO_BE=SaaSLTB,
                                SCHOOL_MODE=SaaSSchoolMode,
                                SCHOOL_OPERATE=SaaSSOperate,
                                SCHOOL_LOCALITY=SaaSSchoolArea,
                                location=Point(SaaSSchoolLongitude, SaaSSchoolLatitude),
                                #SCHOOL_CITY=SaaSSchoolCity,
                                BUSINESS=SaaSBusiness,
                                SCHOOL_NAME=SaaSSchoolName,
                                SCHOOL_WEBSITE=SaaSSchoolWebsite,
                                SCHOOL_FB=SaaSSchoolFB,
                                LINKEDIN=SaaSLinkedin,
                                OCCUPATION=SaaSOccupation,
                                PASSION=SaaSPassion,
                                WHY_AFFILIATE=SaaSWhyAffiliate
                            )
                new_mschool.save()
                #store some details in USER_DETAILS from the application and social_account
                new_user_details=USER_DETAILS(
                                    uid=social_data.uid,
                                    FULL_NAME=SaaSName,
                                    USER_EMAIL=SaaSEmail,
                                    CONTACT_PHONE=SaaSPhone,
                                    PHONE_CTRY_CODE=SaaSCountryCode,
                                    AUTH_TYPE=1,
                                    IS_MICROSCHOOL="Y",
                                    PHOTO_URL=social_data.extra_data["picture"]                     
                                )
                new_user_details.save()

            else:
                #store all the data in both QUEST_APPLN and MICRO_APPLN table
                new_qschool=QUEST_APPLN(
                                uid=social_data.uid,
                                IS_COMPLETE="Y",
                                NAME=SaaSName,
                                DOB=SaaSDOB,
                                EMAIL=SaaSEmail,
                                COUNTRY_CODE=SaaSCountryCode,
                                PHONE=SaaSPhone,
                                LOVE_TO_BE=SaaSLTB,
                                SCHOOL_MODE=SaaSSchoolMode,
                                SCHOOL_OPERATE=SaaSSOperate,
                                SCHOOL_AREA=SaaSSchoolArea,
                                SCHOOL_CITY=SaaSSchoolCity,
                                BUSINESS=SaaSBusiness,
                                SCHOOL_NAME=SaaSSchoolName,
                                SCHOOL_WEBSITE=SaaSSchoolWebsite,
                                SCHOOL_FB=SaaSSchoolFB,
                                LINKEDIN=SaaSLinkedin,
                                OCCUPATION=SaaSOccupation,
                                PASSION=SaaSPassion,
                                WHY_AFFILIATE=SaaSWhyAffiliate
                            )
                new_qschool.save()

                new_mschool=MICRO_APPLY(
                                uid=social_data.uid,
                                IS_COMPLETE="Y",
                                NAME=SaaSName,
                                DOB=SaaSDOB,
                                EMAIL=SaaSEmail,
                                COUNTRY_CODE=SaaSCountryCode,
                                PHONE=SaaSPhone,
                                LOVE_TO_BE=SaaSLTB,
                                SCHOOL_MODE=SaaSSchoolMode,
                                SCHOOL_OPERATE=SaaSSOperate,
                                SCHOOL_LOCALITY=SaaSSchoolArea,
                                location=Point(SaaSSchoolLongitude, SaaSSchoolLatitude),
                                #SCHOOL_CITY=SaaSSchoolCity,
                                BUSINESS=SaaSBusiness,
                                SCHOOL_NAME=SaaSSchoolName,
                                SCHOOL_WEBSITE=SaaSSchoolWebsite,
                                SCHOOL_FB=SaaSSchoolFB,
                                LINKEDIN=SaaSLinkedin,
                                OCCUPATION=SaaSOccupation,
                                PASSION=SaaSPassion,
                                WHY_AFFILIATE=SaaSWhyAffiliate
                            )
                new_mschool.save()
                #store some details in USER_DETAILS from the application and social_account
                new_user_details=USER_DETAILS(
                                    uid=social_data.uid,
                                    FULL_NAME=SaaSName,
                                    USER_EMAIL=SaaSEmail,
                                    CONTACT_PHONE=SaaSPhone,
                                    PHONE_CTRY_CODE=SaaSCountryCode,
                                    AUTH_TYPE=1,
                                    IS_MICROSCHOOL="Y",
                                    IS_QUESTSCHOOL="Y",
                                    PHOTO_URL=social_data.extra_data["picture"]                     
                                )
                new_user_details.save()
            
        else:
            #if Business is NO then don't get school name, website, fb and store other values in db
            #check whether love to become is microschool or questschool
            if SaaSLTB=="Questschool":
                #store all the data in QUEST_APPLN table
                new_qschool=QUEST_APPLN(
                                uid=social_data.uid,
                                IS_COMPLETE="Y",
                                NAME=SaaSName,
                                DOB=SaaSDOB,
                                EMAIL=SaaSEmail,
                                COUNTRY_CODE=SaaSCountryCode,
                                PHONE=SaaSPhone,
                                LOVE_TO_BE=SaaSLTB,
                                SCHOOL_MODE=SaaSSchoolMode,
                                SCHOOL_OPERATE=SaaSSOperate,
                                SCHOOL_AREA=SaaSSchoolArea,
                                SCHOOL_CITY=SaaSSchoolCity,
                                BUSINESS=SaaSBusiness,
                                LINKEDIN=SaaSLinkedin,
                                OCCUPATION=SaaSOccupation,
                                PASSION=SaaSPassion,
                                WHY_AFFILIATE=SaaSWhyAffiliate
                            )
                new_qschool.save()
                #store some details in USER_DETAILS from the application and social_account
                new_user_details=USER_DETAILS(
                                    uid=social_data.uid,
                                    FULL_NAME=SaaSName,
                                    USER_EMAIL=SaaSEmail,
                                    CONTACT_PHONE=SaaSPhone,
                                    PHONE_CTRY_CODE=SaaSCountryCode,
                                    AUTH_TYPE=1,
                                    IS_QUESTSCHOOL="Y",
                                    PHOTO_URL=social_data.extra_data["picture"]                     
                                )
                new_user_details.save()
            elif SaaSLTB=="Microschool":
                #store all the data in MICRO_APPLN table
                new_mschool=MICRO_APPLY(
                                uid=social_data.uid,
                                IS_COMPLETE="Y",
                                NAME=SaaSName,
                                DOB=SaaSDOB,
                                EMAIL=SaaSEmail,
                                COUNTRY_CODE=SaaSCountryCode,
                                PHONE=SaaSPhone,
                                LOVE_TO_BE=SaaSLTB,
                                SCHOOL_MODE=SaaSSchoolMode,
                                SCHOOL_OPERATE=SaaSSOperate,
                                SCHOOL_LOCALITY=SaaSSchoolArea,
                                location=Point(SaaSSchoolLongitude, SaaSSchoolLatitude),
                                #SCHOOL_CITY=SaaSSchoolCity,
                                BUSINESS=SaaSBusiness,
                                LINKEDIN=SaaSLinkedin,
                                OCCUPATION=SaaSOccupation,
                                PASSION=SaaSPassion,
                                WHY_AFFILIATE=SaaSWhyAffiliate
                            )
                new_mschool.save()
                #store some details in USER_DETAILS from the application and social_account
                new_user_details=USER_DETAILS(
                                    uid=social_data.uid,
                                    FULL_NAME=SaaSName,
                                    USER_EMAIL=SaaSEmail,
                                    CONTACT_PHONE=SaaSPhone,
                                    PHONE_CTRY_CODE=SaaSCountryCode,
                                    AUTH_TYPE=1,
                                    IS_MICROSCHOOL="Y",
                                    PHOTO_URL=social_data.extra_data["picture"]                     
                                )
                new_user_details.save()
            else:
                #store all the data in both QUEST_APPLN and MICRO_APPLN table
                new_qschool=QUEST_APPLN(
                                uid=social_data.uid,
                                IS_COMPLETE="Y",
                                NAME=SaaSName,
                                DOB=SaaSDOB,
                                EMAIL=SaaSEmail,
                                COUNTRY_CODE=SaaSCountryCode,
                                PHONE=SaaSPhone,
                                LOVE_TO_BE=SaaSLTB,
                                SCHOOL_MODE=SaaSSchoolMode,
                                SCHOOL_OPERATE=SaaSSOperate,
                                SCHOOL_AREA=SaaSSchoolArea,
                                SCHOOL_CITY=SaaSSchoolCity,
                                BUSINESS=SaaSBusiness,
                                LINKEDIN=SaaSLinkedin,
                                OCCUPATION=SaaSOccupation,
                                PASSION=SaaSPassion,
                                WHY_AFFILIATE=SaaSWhyAffiliate
                            )
                new_qschool.save()

                new_mschool=MICRO_APPLY(
                                uid=social_data.uid,
                                IS_COMPLETE="Y",
                                NAME=SaaSName,
                                DOB=SaaSDOB,
                                EMAIL=SaaSEmail,
                                COUNTRY_CODE=SaaSCountryCode,
                                PHONE=SaaSPhone,
                                LOVE_TO_BE=SaaSLTB,
                                SCHOOL_MODE=SaaSSchoolMode,
                                SCHOOL_OPERATE=SaaSSOperate,
                                SCHOOL_LOCALITY=SaaSSchoolArea,
                                location=Point(SaaSSchoolLongitude, SaaSSchoolLatitude),
                                #SCHOOL_CITY=SaaSSchoolCity,
                                BUSINESS=SaaSBusiness,
                                LINKEDIN=SaaSLinkedin,
                                OCCUPATION=SaaSOccupation,
                                PASSION=SaaSPassion,
                                WHY_AFFILIATE=SaaSWhyAffiliate
                            )
                new_mschool.save()
                #store some details in USER_DETAILS from the application and social_account
                new_user_details=USER_DETAILS(
                                    uid=social_data.uid,
                                    FULL_NAME=SaaSName,
                                    USER_EMAIL=SaaSEmail,
                                    CONTACT_PHONE=SaaSPhone,
                                    PHONE_CTRY_CODE=SaaSCountryCode,
                                    AUTH_TYPE=1,
                                    IS_MICROSCHOOL="Y",
                                    IS_QUESTSCHOOL="Y",
                                    PHOTO_URL=social_data.extra_data["picture"]                     
                                )
                new_user_details.save()
        #send email of application received
        subject='Application Received!'
        html_template='socialaccount/email/application_received_email.html'
        html_message=render_to_string(html_template)
        to_email=user.email
        message=EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [to_email])
        message.content_subtype='html'
        message.send()
        return redirect('audition')

@login_required
def audition(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    if USER_DETAILS.objects.filter(USER_EMAIL=user.email):
        user_details=USER_DETAILS.objects.get(USER_EMAIL=user.email)
        if user_details.IS_MICROSCHOOL=="Y" or user_details.IS_QUESTSCHOOL=="Y":
            #only show audition form if one of the application is submitted
            if user_details.IS_MICROSCHOOL=="Y":
                #ask for financial field in form because it is microschool
                if MICRO_AUDN.objects.filter(uid=user_details.uid):
                    #check if user has already submitted audition
                    #pass a variable with done so that it can be used in frontend to show message that this user is already registered
                    return render(request, 'audition.html',{'audition_done':'done'})
                else:
                    return render(request, 'audition.html',{'financial':'yes'})
            elif user_details.IS_MICROSCHOOL=="Y" and user_details.IS_QUESTSCHOOL=="Y":
                #ask for financial field in form because it is both microschool and questschool
                if MICRO_AUDN.objects.filter(uid=user_details.uid) and QUEST_AUDN.objects.filter(uid=user_details.uid):
                    #check if user has already submitted audition
                    #pass a variable with done so that it can be used in frontend to show message that this user is already registered
                    return render(request, 'audition.html',{'audition_done':'done'})
                else:
                    return render(request, 'audition.html',{'financial':'yes'})
            else:
                #it is a questschool so don't ask for financial field
                if QUEST_AUDN.objects.filter(uid=user_details.uid):
                    #check if user has already submitted audition
                    #pass a variable with done so that it can be used in frontend to show message that this user is already registered
                    return render(request, 'audition.html',{'audition_done':'done'})
                else:
                    return render(request, 'audition.html',{'financial':'no'})
        else:
            #show application form
            return redirect('apply')
    else:
        return redirect('apply')

@login_required
def saasaudition(request):
    if request.method == "POST":
        user_id=request.session['user_id']
        user=User.objects.get(id=user_id)
        user_details=USER_DETAILS.objects.get(USER_EMAIL=user.email)

        SaaSESF=request.POST['SaaSESF']
        SaaSCodingSkill=request.POST['SaaSCodingSkill']
        SaaSPhotoSkill=request.POST['SaaSPhotoSkill']
        SaaSVideoSkill=request.POST['SaaSVideoSkill']
        SaaSPassionToLearn=request.POST['SaaSPassionToLearn']
        SaaSHDWC=request.POST['SaaSHDWC']
        SaaSModeInternet=request.POST['SaaSModeInternet']
        SaaSSpeed=request.POST['SaaSSpeed']
        SaaSYoutubeLink=request.POST['SaaSYoutubeLink']
        SaaSNoOfStu=request.POST['SaaSNoOfStu']
        SaaSQuestions=request.POST['SaaSQuestions']

        if user_details.IS_MICROSCHOOL=="Y" and user_details.IS_QUESTSCHOOL=="N":
            #store in MICRO_AUDN table only
            SaaSFinancial=request.POST['SaaSFinancial']
            SaaSFromWhere=request.POST['SaaSFromWhere']
            new_maudition=MICRO_AUDN(
                            uid=user_details.uid,
                            IS_COMPLETE="Y",
                            ENGLISH_FLUENCY=SaaSESF,
                            CODING_SKILL=SaaSCodingSkill,
                            PHOTO_EDITING=SaaSPhotoSkill,
                            VIDEO_EDITING=SaaSVideoSkill,
                            PASSION_TO_LEARN=SaaSPassionToLearn,
                            FINANCIAL_MONEY_REQUIRED=SaaSFinancial,
                            MONEY_COME_FROM=SaaSFromWhere,
                            HD_WEBCAM=SaaSHDWC,
                            INTERNET_MODE=SaaSModeInternet,
                            INTERNET_SPEED=SaaSSpeed,
                            YOUTUBE_VIDEO=SaaSYoutubeLink,
                            NO_OF_STUDENTS=SaaSNoOfStu,
                            QUESTIONS=SaaSQuestions
                          )
            new_maudition.save()
        elif user_details.IS_QUESTSCHOOL=="Y" and user_details.IS_MICROSCHOOL=="N":
            #store in QUEST_AUDN table only
            new_qaudition=QUEST_AUDN(
                            uid=user_details.uid,
                            IS_COMPLETE="Y",
                            ENGLISH_FLUENCY=SaaSESF,
                            CODING_SKILL=SaaSCodingSkill,
                            PHOTO_EDITING=SaaSPhotoSkill,
                            VIDEO_EDITING=SaaSVideoSkill,
                            PASSION_TO_LEARN=SaaSPassionToLearn,
                            HD_WEBCAM=SaaSHDWC,
                            INTERNET_MODE=SaaSModeInternet,
                            INTERNET_SPEED=SaaSSpeed,
                            YOUTUBE_VIDEO=SaaSYoutubeLink,
                            NO_OF_STUDENTS=SaaSNoOfStu,
                            QUESTIONS=SaaSQuestions
                          )
            new_qaudition.save()
        elif user_details.IS_MICROSCHOOL=="Y" and user_details.IS_QUESTSCHOOL=="Y":
            #store in both MICRO_AUDN and QUEST_AUDN table
            print("bothhhhhhhhhhh")
            SaaSFinancial=request.POST['SaaSFinancial']
            SaaSFromWhere=request.POST['SaaSFromWhere']
            new_maudition=MICRO_AUDN(
                            uid=user_details.uid,
                            IS_COMPLETE="Y",
                            ENGLISH_FLUENCY=SaaSESF,
                            CODING_SKILL=SaaSCodingSkill,
                            PHOTO_EDITING=SaaSPhotoSkill,
                            VIDEO_EDITING=SaaSVideoSkill,
                            PASSION_TO_LEARN=SaaSPassionToLearn,
                            FINANCIAL_MONEY_REQUIRED=SaaSFinancial,
                            MONEY_COME_FROM=SaaSFromWhere,
                            HD_WEBCAM=SaaSHDWC,
                            INTERNET_MODE=SaaSModeInternet,
                            INTERNET_SPEED=SaaSSpeed,
                            YOUTUBE_VIDEO=SaaSYoutubeLink,
                            NO_OF_STUDENTS=SaaSNoOfStu,
                            QUESTIONS=SaaSQuestions
                          )
            new_maudition.save()

            new_qaudition=QUEST_AUDN(
                            uid=user_details.uid,
                            IS_COMPLETE="Y",
                            ENGLISH_FLUENCY=SaaSESF,
                            CODING_SKILL=SaaSCodingSkill,
                            PHOTO_EDITING=SaaSPhotoSkill,
                            VIDEO_EDITING=SaaSVideoSkill,
                            PASSION_TO_LEARN=SaaSPassionToLearn,
                            HD_WEBCAM=SaaSHDWC,
                            INTERNET_MODE=SaaSModeInternet,
                            INTERNET_SPEED=SaaSSpeed,
                            YOUTUBE_VIDEO=SaaSYoutubeLink,
                            NO_OF_STUDENTS=SaaSNoOfStu,
                            QUESTIONS=SaaSQuestions
                          )
            new_qaudition.save()
        #send email of audition received
        subject='Geekz SaaS Audition Completed!'
        html_template='socialaccount/email/audition_completed_email.html'
        html_message=render_to_string(html_template)
        to_email=user.email
        message=EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [to_email])
        message.content_subtype='html'
        message.send()
        return redirect('profiling')

@login_required
def student_profileEdit(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    print(user)
    user_details=USER_DETAILS.objects.filter(USER_EMAIL=user.email)    
    print(user_details) 
    if request.method == "POST":
        SaaSName=request.POST['SaaSName']
        #SaaSEmail=request.POST['SaaSEmail']
        SaaSPhone=request.POST['SaaSPhone']
        user_id=request.session['user_id']
        user=User.objects.get(id=user_id)
        user_details=USER_DETAILS.objects.get(USER_EMAIL=user.email)
        user_details.FULL_NAME = SaaSName
        user_details.CONTACT_PHONE = SaaSPhone
        user_details.save(update_fields=['FULL_NAME','CONTACT_PHONE'])
        return redirect('index')
    return render(request,"student_profileEdit.html",{"object_details":user_details})  


####################Django calendar #########################
#Django calendar_admin view to add slots

def schedule_admin(request):
    if request.method == "POST" :
        start_time = request.POST['start_time']
        print(start_time)
        end_time = request.POST['end_time']
        day = request.POST['day']
        time_duration = float(request.POST['duration'])
        start_datetime_object =  datetime.datetime.strptime(start_time, '%H:%M')
        end_datetime_object =  datetime.datetime.strptime(end_time, '%H:%M')
        #start_datetime_object = start_datetime_object.astimezone(timezone('Asia/Kolkata'))
        #end_datetime_object = end_datetime_object.astimezone(timezone('Asia/Kolkata'))
        def time_slots(start_time, end_time,duration):
            t = start_time
            while t < end_time:
                yield t.strftime('%H:%M')
                t += datetime.timedelta(minutes=time_duration)
                slot_obj = SLOTS_DAY(slot=t.strftime('%H:%M'),day=day,duration=time_duration,admin="admin")
                slot_obj.save()
                print(t.strftime('%H:%M'))
        print(list(time_slots(start_datetime_object, end_datetime_object,time_duration)))
        return render(request,'schedule_admin.html')
    slots_monday = SLOTS_DAY.objects.filter(day='Monday')
    slots_tuesday = SLOTS_DAY.objects.filter(day='Tuesday') 
    slots_wednesday = SLOTS_DAY.objects.filter(day='Wednesday')
    slots_thursday = SLOTS_DAY.objects.filter(day='Thursday')
    slots_friday = SLOTS_DAY.objects.filter(day='Friday')
    slots_saturday = SLOTS_DAY.objects.filter(day='Saturday')
    return render(request,'schedule_admin.html',{'slots_monday':slots_monday,'slots_tuesday':slots_tuesday,'slots_wednesday':slots_wednesday,'slots_thursday':slots_thursday,'slots_friday':slots_friday,'slots_saturday':slots_saturday}) 
'''
# view to create event and to write in google calendar and create google meet link
def create_event(request):    
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time
        )
         #################### google calendar integration ###################
        service_account_email = "geekz-145@geekz-297209.iam.gserviceaccount.com"
        SCOPES = ["https://www.googleapis.com/auth/calendar"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name( filename="client_secret.json", scopes=SCOPES )
        def build_service():
            service = build("calendar", "v3", credentials=credentials)
            return service

        def create_event():
            service = build_service()
            #start_datetime = datetime.datetime.now(tz=pytz.utc)
            event_cal = (service.events().insert(calendarId="c27hrqb165rc6s5mgoqq5l1e4c@group.calendar.google.com",body={
                "summary": title,
                "description": description,
                "start":{"dateTime":start_time.isoformat()}, 
                "end": {
                    "dateTime": end_time.isoformat()
                },
                "conferenceData": {"createRequest": {"requestId": f"{uuid4().hex}",
                                                      "conferenceSolutionKey": {"type": "hangoutsMeet"}}},
                "reminders": {"useDefault": True},
            },conferenceDataVersion=1).execute() )
            print("ee",event_cal['entryPoints'][0]['uri']) ## trying to fetch google meet link from event_cal 

        create_event()
        send_mail(
            "events",
            "The audition date is booked ",
            settings.EMAIL_HOST_USER,
            ['chauhanreetika45@gmail.com']
        )
        return HttpResponseRedirect(reverse('calendarapp:calendar'))
    return render(request, 'event.html', {'form': form})
'''
# view for user to pick date and select slot
@login_required
def saasappointment(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    user_details=USER_DETAILS.objects.get(USER_EMAIL=user.email)
    micro_audition = MICRO_AUDN.objects.get(uid = user_details.uid)
    microprofil = MICRO_PROFILIN.objects.filter(uid = user_details.uid )
    '''if user_details.IS_MICROSCHOOL=="Y" or user_details.IS_QUESTSCHOOL=="Y" and micro_audition.IS_COMPLETE=='Y' and micro_audition.IS_APPROVED == 'N':
        return redirect("apply")'''
    if user_details.IS_MICROSCHOOL=="Y" or user_details.IS_QUESTSCHOOL=="Y" and micro_audition.IS_COMPLETE=='Y' :
        if not microprofil:
            if request.method == 'POST':
                # create a form instance and populate it with data from the request:
                user_id=request.session['user_id']
                user=User.objects.get(id=user_id)
                user_details=USER_DETAILS.objects.get(USER_EMAIL=user.email)
                print(user)
                print(user.email)
                form = SlotCreationForm(request.POST)
                # check whether it's valid:
                if form.is_valid():
                    schedule_date = form.cleaned_data['schedule_date']
                    slot = form.cleaned_data['slot']
                    print('sc',type(schedule_date))
                    print('slot',slot)
                    print(type(slot))
                    slot_obj = SLOTS_DAY.objects.filter(id=slot.id)
                    print('slot_obj',slot_obj)
                    qq = list(slot_obj)
                    print(qq)
                    qq = qq[0]
                    nn = qq.duration
                    start_time = qq.slot
                    now = datetime.datetime.now()
                    date_obj = schedule_date.strftime("%Y-%m-%d")
                    datee = schedule_date.strftime("%b %d %Y")
                    print(datee)
                    print(type(date_obj))
                    print(type(qq.slot))
                    start = datetime.datetime.strptime(qq.slot, '%H:%M')
                    end = start + datetime.timedelta(minutes=float(nn))
                    start = start.strftime("%I:%M %p")
                    end = end.strftime("%I:%M %p")
                    start_time = date_obj + " "+ start_time 
                    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')
                    end_time = start_time + datetime.timedelta(minutes=float(nn))
                    start_time = start_time.astimezone(timezone('Asia/Kolkata')) # time zone attached
                    end_time = end_time.astimezone(timezone('Asia/Kolkata'))   # time zone attached
                    print('st',start)
                    print('et', end_time)
                    print("type",type(start_time))
                    heading = qq.day + " " + datee + " " + "at" + " " + start + " " + "to" + " " + end
                    link = " "
                    if schedule_date < datetime.date.today():
                        return HttpResponse("Please do not enter past date")    
                    else:
                        service_account_email = "geekz-145@geekz-297209.iam.gserviceaccount.com"
                        SCOPES = ["https://www.googleapis.com/auth/calendar"]
                        credentials = ServiceAccountCredentials.from_json_keyfile_name( filename="client_secret.json", scopes=SCOPES )
                        def build_service():
                            service = build("calendar", "v3", credentials=credentials)
                            return service
                        
                        def create_event():
                            service = build_service()
                            event_cal = (service.events().insert(calendarId="c27hrqb165rc6s5mgoqq5l1e4c@group.calendar.google.com",body={
                            "summary": "GEEKZ",
                            "description": "GEEKZ INTERVIEW FOR AFFLIATION",
                            "start":{"dateTime":start_time.isoformat()}, 
                            "end": {
                                "dateTime": end_time.isoformat()
                                    },
                            "conferenceData": {"createRequest": {"requestId": f"{uuid4().hex}",
                                                            "conferenceSolutionKey": {"type": "hangoutsMeet"}}},
                            "reminders": {"useDefault": True},
                            "attendees":user.email,

                                },conferenceDataVersion=1).execute() )
                            
                            print("ee",event_cal) 
                            create_event.link = event_cal['hangoutLink'] ##  fetch google meet link from event_cal 
                            profiling_obj = MICRO_PROFILIN(uid = user_details.uid, IS_PROFILINGCOMPLETE='Y',USER = user.email , EVENT_ID = event_cal['id'],ICalUID=event_cal['iCalUID'],hangoutLink = create_event.link,START_TIME= event_cal['start']['dateTime'],END_TIME = event_cal['end']['dateTime'],HEADING= heading,slot= qq,schedule_date= schedule_date)
                            profiling_obj.save()
                            subject='Geekz SaaS Profiling Confirmation'
                            html_template='socialaccount/email/SaaS_Profiling_Confirmation_Email.html'
                            html_message=render_to_string(html_template,{'heading':heading})
                            to_email= user.email
                            message=EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [to_email])
                            message.content_subtype='html'
                            message.send()
                        create_event()
                        return render(request,"joinMeeting.html",{'link':create_event.link,'heading':heading})        
            # if a GET (or any other method) we'll create a blank form
            else:
                form = SlotCreationForm()
                return render(request,"profiling.html",{'form': form})
        else:
            micro_profiling = MICRO_PROFILIN.objects.get(uid = user_details.uid )
            return render(request,"joinMeeting.html",{'link':micro_profiling.hangoutLink,'heading':micro_profiling.HEADING})


def deletevent(request):
    if request.method == "POST" :
        user_id=request.session['user_id']
        user=User.objects.get(id=user_id)
        micro_prof = MICRO_PROFILIN.objects.get(USER = user.email )
        SaaSreason=request.POST['reason']
        reason_ob = RESCHEDULE_REASON(uid = micro_prof.uid,reason=SaaSreason)
        reason_ob.save()
        service_account_email = "geekz-145@geekz-297209.iam.gserviceaccount.com"
        SCOPES = ["https://www.googleapis.com/auth/calendar"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name( filename="client_secret.json", scopes=SCOPES )
        def build_service():
            service = build("calendar", "v3", credentials=credentials)
            return service
                        
        def create_event():
            service = build_service()
            event_cal = (service.events().delete(calendarId="c27hrqb165rc6s5mgoqq5l1e4c@group.calendar.google.com",eventId = micro_prof.EVENT_ID).execute() )     
        create_event()
        MICRO_PROFILIN.objects.filter(uid = micro_prof.uid).delete()
        form = SlotCreationForm()
        return render(request,"profiling.html",{'form': form})
# ajax view to get slots and populate in dropdown and reading calendar to filter slots
def load_slots(request):
    print("fffffffffff")
    day = request.GET.get('day_id')
    print(day)
    ####################Reading Calendar###############################
    service_account_email = "geekz-145@geekz-297209.iam.gserviceaccount.com"
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name( filename="client_secret.json", scopes=SCOPES )
    def build_service():
        service = build("calendar", "v3", credentials=credentials)
        return service
    page_token = None
    while True:
        service = build_service()
        events = service.events().list(calendarId='c27hrqb165rc6s5mgoqq5l1e4c@group.calendar.google.com', pageToken=page_token).execute()
        times =[]
        summery = []
        for event in events['items']:
            print (event['start']['dateTime'])
            times.append(event['start']['dateTime'])
            summery.append(event['summary'])
        print(times)
        print(summery)    
        page_token = events.get('nextPageToken')
        if not page_token:
            break
    #################################################
    def findDay(date):
        born = datetime.datetime.strptime(date, '%Y-%m-%d').weekday() 
        return (calendar.day_name[born]) 
    slots = SLOTS_DAY.objects.filter(day=findDay(day)).all()
    print(slots)
    slots_obj = list(slots)
    slot_fil = []
    for s in slots_obj:
        print("slots",s.slot)
        #now = datetime.datetime.now()
        #date_obj = now.strftime("%Y-%m-%d")
        #print(date_obj)
        date_obj = day + " "+ s.slot
        print(date_obj)
        start_time = datetime.datetime.strptime(date_obj, '%Y-%m-%d %H:%M')
        start_time = start_time.astimezone(timezone('Asia/Kolkata'))
        print(start_time.isoformat())
        start_time = start_time.isoformat()
        # filtering slots if the slot is booked
        for gc in times:
            if start_time == gc:
                print("i am already in google calendar")
                flag ="false"
                break
            else:
                print("i am in else")
                print("gc",gc)
                flag = "true"
                print("start_time",start_time)
        print(flag)            
        if flag == "true":
            slot_fil.append(s)
    print(slot_fil)            
    return render(request, 'slots_dropdown_list_options.html', {'slots': slot_fil}) 
    

################################### auto creation of webpage ##########################
@login_required
@allowed_users(allowed_roles=['admin'])
def web_form(request):
    if request.method == "POST" and  request.FILES['profile']:
        user_id=request.session['user_id']
        user=User.objects.get(id=user_id)
        url = request.POST['url']
        title = request.POST['title']
        m1 = request.POST['m1']
        m2 = request.POST['m2']
        m3 = request.POST['m3']
        schoolfee = request.POST['schoolfee']
        brand = request.POST['brand']
        profile = request.FILES['profile']
        ob = webdata21(url = url ,title = title ,Infrastructure_affliation = m1,Education_affliation=m2,HomeSchool_affliation=m3, School_Fee_rule=schoolfee,brandFee_rule=brand, profile = profile,admin_email=user.email)
        ob.save()
        #OBJ = webdata2.objects.filter(url=url)
        return render(request,'index.html')
    return render(request,'web_form.html')

@login_required
@allowed_users(allowed_roles=['superadmin'])
def webpage_creation(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    OBJ = webdata21.objects.all()
    return render(request,'webpage_creation.html',{'ob':OBJ})

@login_required
@allowed_users(allowed_roles=['superadmin'])
def webpage(request,url):
        print('url',url)
        l = webdata21.objects.filter(url=url)
        return render(request, 'webpage.html',{'l':l})  




 ###########################################3       
