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
from .forms import SlotCreationForm,IndividualSlotCreationForm
from uuid import uuid4
import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from .decorators import  allowed_users
from django.contrib.auth.models import Group
from schoolasaservice.utils import render_to_pdf
from django.http import HttpResponse
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
from django.views import View
from .forms import PhotoForm
from .models import Photo_webpage1
from django.contrib.gis.measure import Distance
from django.contrib.gis.geos import Point
from django.db.models.query import QuerySet


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
                    micro_audition = MICRO_AUDN.objects.get(uid = user_details.uid) 
                    #check if user has already submitted audition
                    #pass a variable with done so that it can be used in frontend to show message that this user is already registered
                    if micro_audition.IS_APPROVED =='N':
                        return render(request, 'audition.html',{'audition_done':'done'})
                    elif micro_audition.IS_APPROVED =='Y':
                        return redirect('profiling')    
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
def profiling(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    if USER_DETAILS.objects.filter(USER_EMAIL=user.email):
        user_details=USER_DETAILS.objects.get(USER_EMAIL=user.email)
        micro_audition = MICRO_AUDN.objects.filter(uid = user_details.uid,IS_COMPLETE='Y',IS_APPROVED ='Y')
        if micro_audition:
            microprofil = MICRO_PROFILIN.objects.filter(uid = user_details.uid )
            if not microprofil:
                print("hiii")
                form = SlotCreationForm()
                return render(request,'profiling.html',{'form':form})
            else:
                micro_profiling = MICRO_PROFILIN.objects.get(uid = user_details.uid )
                return render(request,"joinMeeting.html",{'link':micro_profiling.hangoutLink,'heading':micro_profiling.HEADING})   
        else:
            return redirect('audition')
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
    student_obj = studentApplications.objects.filter(student_id = user.id)
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
    return render(request,"student_profileEdit.html",{"object_details":user_details,'student_obj':student_obj})  


####################Django calendar #########################
#Django calendar_admin view to add slots

def schedule_admin(request):
    if request.method == "POST" :
        start_time = request.POST['start_time']
        print(type(start_time))
        end_time = request.POST['end_time']
        day = request.POST['day']
        time_duration = float(request.POST['duration'])
        start_datetime_object =  datetime.datetime.strptime(start_time, '%H:%M')
        end_datetime_object =  datetime.datetime.strptime(end_time, '%H:%M')
        start_datetime_object = start_datetime_object.strftime("%I:%M %p")
        end_datetime_object = end_datetime_object.strftime("%I:%M %p")
        start_datetime_object =  datetime.datetime.strptime(start_datetime_object, '%I:%M %p')
        end_datetime_object =  datetime.datetime.strptime(end_datetime_object, '%I:%M %p')
        #start_datetime_object = start_datetime_object.astimezone(timezone('Asia/Kolkata'))
        #end_datetime_object = end_datetime_object.astimezone(timezone('Asia/Kolkata'))
        def time_slots(start_datetime_object, end_datetime_object,duration):
            t = start_datetime_object
            while t < end_datetime_object:
                yield t.strftime('%I:%M %p')
                slot_obj = SLOTS_DAY(slot=t.strftime('%I:%M %p'),day=day,duration=time_duration,admin="admin")
                t += datetime.timedelta(minutes=time_duration)
                slot_obj.save()
                print(t.strftime('%I:%M %p'))
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
    if request.method == 'POST':
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
            start = datetime.datetime.strptime(qq.slot, '%I:%M %p')
            end = start + datetime.timedelta(minutes=float(nn))
            start = start.strftime("%I:%M %p")
            end = end.strftime("%I:%M %p")
            start_time = date_obj + " "+ start_time 
            start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %I:%M %p')
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
                service_account_email = "geekzcalendar@geekzcaldendar.iam.gserviceaccount.com"
                SCOPES = ["https://www.googleapis.com/auth/calendar"]
                credentials = ServiceAccountCredentials.from_json_keyfile_name( filename="clientsecret_geekz.json", scopes=SCOPES )
                def build_service():
                    service = build("calendar", "v3", credentials=credentials)
                    return service
                
                def create_event():
                    service = build_service()
                    event_cal = (service.events().insert(calendarId="thkmk74n50mn6kt14hi1qdru58@group.calendar.google.com",body={
                    "summary": "GEEKZ",
                    "description": "GEEKZ INTERVIEW FOR AFFLIATION",
                    "start":{"dateTime":start_time.isoformat()}, 
                    "end": {
                        "dateTime": end_time.isoformat()
                            },
                    #"conferenceData": {"createRequest": {"requestId": "7qxalsvy0e",
                    #                                "conferenceSolutionKey": {"type": "eventNamedHangout"}}},
                    "reminders": {"useDefault": True},
                    "attendees":user.email,

                        #},conferenceDataVersion=1).execute())
                        }).execute())       
                    print("ee",event_cal) 
                    #create_event.link = event_cal['hangoutLink'] ##  fetch google meet link from event_cal 
                    #profiling_obj = MICRO_PROFILIN(uid = user_details.uid, IS_PROFILINGCOMPLETE='Y',USER = user.email , EVENT_ID = event_cal['id'],ICalUID=event_cal['iCalUID'],hangoutLink = create_event.link,START_TIME= event_cal['start']['dateTime'],END_TIME = event_cal['end']['dateTime'],HEADING= heading,slot= qq,schedule_date= schedule_date)
                    profiling_obj = MICRO_PROFILING(uid = user_details.uid, IS_PROFILINGCOMPLETE='Y',USER = user.email , EVENT_ID = event_cal['id'],ICalUID=event_cal['iCalUID'],START_TIME= event_cal['start']['dateTime'],END_TIME = event_cal['end']['dateTime'],HEADING= heading,slot= qq,schedule_date= schedule_date,hangoutLink = "not")
                    profiling_obj.save()
                    subject='Geekz SaaS Profiling Confirmation'
                    html_template='socialaccount/email/SaaS_profiling_copy.html'
                    html_message=render_to_string(html_template,{'heading':heading,'uid':user_details.uid})
                    to_email= user.email
                    message=EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [to_email])
                    message.content_subtype='html'
                    message.send()
                create_event()
                return render(request,"joinMeeting.html",{'heading':heading})  

def deletevent(request):
    if request.method == "POST" :
        user_id=request.session['user_id']
        user=User.objects.get(id=user_id)
        micro_prof = MICRO_PROFILING.objects.get(USER = user.email )
        SaaSreason=request.POST['reason']
        reason_ob = RESCHEDULE_REASON(uid = micro_prof.uid,reason=SaaSreason)
        reason_ob.save()
        service_account_email = "geekzcalendar@geekzcaldendar.iam.gserviceaccount.com"
        SCOPES = ["https://www.googleapis.com/auth/calendar"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name( filename="clientsecret_geekz.json", scopes=SCOPES )
        def build_service():
            service = build("calendar", "v3", credentials=credentials)
            return service
                        
        def create_event():
            service = build_service()
            event_cal = (service.events().delete(calendarId="thkmk74n50mn6kt14hi1qdru58@group.calendar.google.com",eventId = micro_prof.EVENT_ID).execute() )     
        create_event()
        MICRO_PROFILING.objects.filter(uid = micro_prof.uid).delete()
        form = SlotCreationForm()
        return render(request,"profiling.html",{'form': form})


# ajax view to get slots and populate in dropdown and reading calendar to filter slots
def load_slots(request):
    print("fffffffffff")
    day = request.GET.get('day_id')
    print(day)
    ####################Reading Calendar###############################
    service_account_email = "geekzcalendar@geekzcaldendar.iam.gserviceaccount.com"
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name( filename="clientsecret_geekz.json", scopes=SCOPES )
    def build_service():
        service = build("calendar", "v3", credentials=credentials)
        return service
    page_token = None
    while True:
        service = build_service()
        events = service.events().list(calendarId='thkmk74n50mn6kt14hi1qdru58@group.calendar.google.com', pageToken=page_token).execute()
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
        start_time = datetime.datetime.strptime(date_obj, '%Y-%m-%d %I:%M %p')
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
#@login_required
#@allowed_users(allowed_roles=['admin'])
def web_form(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    user_details=USER_DETAILS.objects.get(USER_EMAIL=user.email)
    IE=INDIVIDUAL_WEBPAGESS1.objects.filter(uid=user_details.uid,IS_COMPLETE='N',IS_APPROVED ='N')
    print(IE)
     # msg form to be reviewed
    
    IE1 = INDIVIDUAL_WEBPAGESS1.objects.filter(uid=user_details.uid,IS_COMPLETE='Y',IS_APPROVED ='Y') # show webpage
    if IE:
        print('hi')
        return redirect('IndividualFeedetails')
        
    if IE1:
        IEE = INDIVIDUAL_WEBPAGESS1.objects.get(uid=user_details.uid)
        LOCALITY = IEE.LOCALITY
        return render(request,'webpage.html',{'l':IE1})
    else:
        print("hey")
        if request.method == "POST" :
            user_id=request.session['user_id']
            user=User.objects.get(id=user_id)
            user_details=USER_DETAILS.objects.get(USER_EMAIL=user.email)
            school_name = request.POST['schoolname']
            is_Spacious_Studio = request.POST['is_Spacious_Studio']
            is_Outdoor_PlayLawn = request.POST['is_Outdoor_PlayLawn']
            is_Commute = request.POST['is_Commute']
            is_WiFi = request.POST['is_WiFi']
            is_Device = request.POST['is_Device']
            is_Food = request.POST['is_Food']
            is_CCTV = request.POST['is_CCTV']
            is_Daycare = request.POST['is_Daycare']
            is_After_School = request.POST['is_After_School']
            is_Residential = request.POST['is_Residential']
            locality = request.POST['locality']                 
            email = request.POST['email']
            phone = request.POST['phone']
            phone1 = request.POST['phone1']
            founder_name1 = request.POST['founder_name1']
            founder_name2 = request.POST['founder_name2']
            about_founder1 = request.POST['about_founder1']
            about_founder2 = request.POST['about_founder2']
            founder_designation =  request.POST['founder_designation']
            founder_designation1 =  request.POST['founder_designation1']
            address1 = request.POST['address1']
            address2 = request.POST['address2']
            SchoolArea = request.POST['SchoolArea']
            googlereview= request.POST['googlereview']
            banner1 = request.FILES['banner1']
           
            def OptimizePics(f):
                try:
                    name = str(f).split('.')[0]
                    
                    image = Image.open(f)
                    image.thumbnail((1500, 1500), Image.ANTIALIAS)
                    thumbnail = BytesIO()
                    # Default quality is quality=75
                    image.save(thumbnail, format='JPEG', quality=80)
                    thumbnail.seek(0)
                    newImage = InMemoryUploadedFile(thumbnail,
                                            None,
                                            name + ".jpg",
                                            'image/jpeg',
                                            thumbnail.tell(),
                                            None)
                    return newImage
                except Exception as e:
                    return e
          
                  
            banner11 =  OptimizePics(banner1)       
            banner2 = request.FILES['banner2']
            banner3 = request.FILES['banner3']
            banner4 = request.FILES['banner4']
            time_from = request.POST['time_from']
            time_from =  datetime.datetime.strptime(time_from, '%H:%M')
            time_from = time_from.strftime("%I:%M %p")
            time_to = request.POST['time_to']
            time_to =  datetime.datetime.strptime(time_to, '%H:%M')
            time_to = time_to.strftime("%I:%M %p")
            time1_from = request.POST['time1_from']
            time1_from =  datetime.datetime.strptime(time1_from, '%H:%M')
            time1_from = time1_from.strftime("%I:%M %p")
            time1_to = request.POST['time1_to']
            time1_to =  datetime.datetime.strptime(time1_to, '%H:%M')
            time1_to = time1_to.strftime("%I:%M %p")
            latitude = request.POST['loc_lat']
            longitude = request.POST['loc_long']
            ob = INDIVIDUAL_WEBPAGESS1(uid = user_details.uid,SCHOOL_NAME = school_name ,LOCALITY = locality ,AMENITIES_is_Spacious_Studio=is_Spacious_Studio ,AMENITIES_is_Outdoor_PlayLawn=is_Outdoor_PlayLawn,AMENITIES_is_Commute = is_Commute,AMENITIES_is_CCTV = is_CCTV,AMENITIES_is_WiFi=is_WiFi,AMENITIES_is_Device=is_Device,AMENITIES_is_Food=is_Food,AMENITIES_is_Daycare=is_Daycare,AMENITIES_is_After_School=is_After_School,AMENITIES_is_Residential= is_Residential,BANNER1=banner11,BANNER2=banner2, BANNER3=banner3,BANNER4=banner4, GOOGLE_REVIEWS_LINK =googlereview,FOUNDER_NAME=founder_name1,DESIGNATION=founder_designation,CO_FOUNDER1=founder_name2,DESIGNATION_CO1=founder_designation1,CONTENT1=about_founder1,CONTENT2=about_founder2,ADDRESS1=address1,ADDRESS2=address2,SCHOOL_LOCALITY =SchoolArea,SCHOOL_PHONE=phone,SCHOOL_PHONE1=phone1,SCHOOL_EMAIL=email,SCHOOL_HOURS_KS=time_from+' to '+ time_to,SCHOOL_HOURS_ES=time1_from+' to '+ time1_to,LATITUDE=latitude,LONGITUDE=longitude)
            ob.save()
            #OBJ = webdata2.objects.filter(url=url)
            return render(request,'individual_feedetails.html')
    
    return render(request,'web_form.html')


def IndividualFeedetails(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    user_details=USER_DETAILS.objects.get(USER_EMAIL=user.email)
    iw = INDIVIDUAL_WEBPAGESS1.objects.filter(uid = user_details.uid)
    iw1 = list(iw)
    iw1 = iw1[0]
    fee = individual_feedetail.objects.filter(admin=iw1)
    if fee:
        return redirect('bulk_load')
    else:
        if request.method == "POST":
            user_id=request.session['user_id']
            user=User.objects.get(id=user_id)
            user_details=USER_DETAILS.objects.get(USER_EMAIL=user.email)
            iw = INDIVIDUAL_WEBPAGESS1.objects.filter(uid = user_details.uid)
            iw1 = list(iw)
            iw1 = iw1[0]
            fullYear_kindergarten = request.POST['fullYear_kindergarten']
            fall_kindergarten = request.POST['fall_kindergarten']
            spring_kindergarten = request.POST['spring_kindergarten']
            fullYear_lowerElementary = request.POST['fullYear_lowerElementary']
            fall_lowerElementary = request.POST['fall_lowerElementary']
            spring_lowerElementary = request.POST['spring_lowerElementary']
            fullYear_UpperElementary = request.POST['fullYear_UpperElementary']
            fall_UpperElementary = request.POST['fall_UpperElementary']
            spring_UpperElementary = request.POST['spring_UpperElementary']
            fee_obj = individual_feedetail(admin=iw1,fullYear_kindergarten=fullYear_kindergarten,fall_kindergarten=fall_kindergarten,spring_kindergarten=spring_kindergarten,fullYear_lowerElementary=fullYear_lowerElementary,fall_lowerElementary=fall_lowerElementary,spring_lowerElementary=spring_lowerElementary,fullYear_UpperElementary=fullYear_UpperElementary,fall_UpperElementary=fall_UpperElementary,spring_UpperElementary=spring_UpperElementary)
            fee_obj.save()
            return render(request,'bulk_load.html')
    return render(request,'individual_feedetails.html')

def web1(request):
    if request.method == "POST" :
        user_id=request.session['user_id']
        user=User.objects.get(id=user_id)
        user_details=USER_DETAILS.objects.get(USER_EMAIL=user.email)
        file = request.FILES['file']
        mm = MyModel1(upload = file ,user = user_details.uid) 
        mm.save()
    return render(request,'web1.html')    

'''@login_required
@allowed_users(allowed_roles=['superadmin'])'''
def webpage_creation(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    uid_obj = USER_DETAILS.objects.get(USER_EMAIL=user.email)
    OBJ = INDIVIDUAL_WEBPAGESS1.objects.all()
    url_obj = INDIVIDUAL_WEBPAGESS1.objects.get(uid = uid_obj.uid)
    url_variable = url_obj.SCHOOL_NAME + url_obj.LOCALITY
    return render(request,'webpage_creation.html',{'ob':OBJ,'URL':url_variable })

'''@login_required
@allowed_users(allowed_roles=['superadmin'])'''
def webpage(request,LOCALITY):
        print('url',LOCALITY)
        l = INDIVIDUAL_WEBPAGESS1.objects.filter(LOCALITY=LOCALITY)
        obj_admin = list(l)
        obj_admin = obj_admin[0]
        user_id=request.session['user_id']
        user=User.objects.get(id=user_id) 
        s_inquiry = InquiryS.objects.filter(uid = user.id)
        if s_inquiry:
            l= INDIVIDUAL_WEBPAGESS1.objects.filter(LOCALITY=LOCALITY) 
            return render(request, 'webpage.html',{'webform_done':'done','l':l})
        else:
            if request.method == "POST" :
                user_id=request.session['user_id']
                user=User.objects.get(id=user_id)
                print(user.id)
                name = request.POST['s_name']
                enrolling_grade = request.POST['enrolling_grade']
                email = request.POST['email']
                phone = request.POST['phone']
                hear_about = request.POST['hear_about']
                school_name = request.POST['school_name']
                inquiry_obj = InquiryS(uid=user.id,studentName=name,enrolling_grade=enrolling_grade,email=email,phone=phone,hear_about_us=hear_about,microschool=school_name)
                inquiry_obj.save()
                
                #### email  to   individual admin #####
                emailadmin = MICRO_APPLY.objects.get(uid=obj_admin.uid)
                subject='Student submitted inquiry'
                html_template='socialaccount/email/admin_emailInquiry.html'
                html_message=render_to_string(html_template)
                to_email= emailadmin.EMAIL
                message=EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [to_email])
                message.content_subtype='html'
                message.send()
                location = INDIVIDUAL_WEBPAGESS1.objects.get(LOCALITY=LOCALITY)
                latitude = location.LATITUDE
                longitude = location.LONGITUDE
                print(type(latitude))
                return redirect('webpage',LOCALITY=location.LOCALITY)
        return render(request, 'webpage.html',{'l':l})


def superAdmin_dashboard(request):
    '''for p in User.objects.raw('SELECT * FROM auth_user'):
        print(p)'''
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    name = user.first_name
    now = datetime.datetime.now()
    auth_obj = User.objects.all().count()   
    auth_obj1 = User.objects.all()  
    print(auth_obj)
    return render(request,'superAdmin_dashboard.html',{'auth_obj':auth_obj,'name': name}) 


def basictables(request):
    auth_obj1 = User.objects.all() 
    return render(request,"bs-basic-table.html",{'auth_obj1':auth_obj1})


@login_required
def individualAdmin_dashboard(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    uid_obj = USER_DETAILS.objects.get(USER_EMAIL=user.email)
    profile = MICRO_APPLY.objects.filter(uid = uid_obj.uid)
    admin_web = INDIVIDUAL_WEBPAGESS1.objects.filter(uid = uid_obj.uid,IS_APPROVED='Y')
    admin_web1 = INDIVIDUAL_WEBPAGESS1.objects.filter(uid = uid_obj.uid,IS_APPROVED='N',IS_COMPLETE="Y")
    webform = ''
    webform_not_APPROVEDYet = ""
    if admin_web1:
        webform_not_APPROVEDYet = "yes"
    elif admin_web:
        webform = 'done'
    return render(request,'individualAdmin_dashboard.html',{'webform': webform,'admin_web':admin_web,'profile':profile,'webform_not_APPROVEDYet':webform_not_APPROVEDYet})

###### Individual Admin approve  student inquiry table #############
def individualAdmin_approvels(request):
    print('hiiiiii')
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    uid_obj = USER_DETAILS.objects.get(USER_EMAIL=user.email)
    profile = MICRO_APPLY.objects.filter(uid = uid_obj.uid)
    admin_web = INDIVIDUAL_WEBPAGESS1.objects.get(uid = uid_obj.uid)
    inquirys = InquiryS.objects.filter(microschool=admin_web.SCHOOL_NAME,ISAPPROVED='N')
    return render(request,"individualAdminDashboard/bs-basicApprovel.html",{'inquirys':inquirys,'profile':profile})

def studentinquiryadmin(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    name = user.first_name
    inquirys = InquiryS.objects.filter(ISAPPROVED='N')
    return render(request,'superAdminDashboard/studentinquiryadmin.html',{'inquirys':inquirys,'name':name})

def requestTC(request,student_id):
    student_obj = studentApplications.objects.get(student_id = student_id)
    subject='Student requesting Tc'
    html_template='socialaccount/email/studentrequestingTc.html'
    html_message=render_to_string(html_template,{'id': student_obj.student_id , 'firstname':student_obj.first_name,'lastname':student_obj.last_name})
    to_email= 'hello@geekz.school'
    message=EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [to_email])
    message.content_subtype='html'
    message.send()



### Student Inquiry Aapprove by Individual Admin
def inquiryApprove(request,uid):
    #user_id=request.session['user_id']
    #user=User.objects.get(id=user_id)
    #uid_obj = USER_DETAILS.objects.get(USER_EMAIL=user.email)
    #admin_web = INDIVIDUAL_WEBPAGESS1.objects.get(uid = uid)
    inquirys = InquiryS.objects.get(uid=uid)
    inquirys.ISAPPROVED ='Y'
    inquirys.save(update_fields=['ISAPPROVED'])
    inquirys_updated = InquiryS.objects.filter(ISAPPROVED='N')
    subject='Inquiry Mail'
    html_template='socialaccount/email/inquirymail.html'
    html_message=render_to_string(html_template,{'microschool': inquirys.microschool})
    to_email= inquirys.email
    message=EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [to_email])
    message.content_subtype='html'
    message.send()
    return redirect('individualAdmin_approvels')

#### landing page #######
def index1(request):
    if request.method == "POST" :
        SaaSLoc_lat=float(request.POST['loc_lat'])
        SaaSLoc_long=float(request.POST['loc_long'])
        user_location = Point(SaaSLoc_long,SaaSLoc_lat)
        cr = MICRO_APPLY.objects.values()
        clients = cr.filter(location__distance_lt=(user_location,Distance(m=5000)))
        print(type(clients))
        print("data",clients)
        cl = list(clients)
        print('hhhhhhhhhhhhhhhhhhhh',cl)
        uid_list = []
        if clients:
            for c in cl:
                print("for loo",c)
                uid_list.append(c['uid'])
            print(uid_list)    
            cl1 = cl[0]
            print(cl1)
            cl2 = cl1['uid']
            print(cl2)
            cards = []
            feeds = []
            for k in uid_list:
                cards_obj = INDIVIDUAL_WEBPAGESS1.objects.filter(uid = k)
                cards_obj1 = INDIVIDUAL_WEBPAGESS1.objects.get(uid = k)
                #feed_obj = feedback_users.objects.filter(school_name=cards_obj1.SCHOOL_NAME).order_by('rating')
                #if feed_obj:
                    #feeds.append(feed_obj)
                cards.append(cards_obj)
            print('objects',cards) 
            #print('feed',feeds)   
            #cards_obj = INDIVIDUAL_WEBPAGESS1.objects.filter(uid = cl2)
            #cards_obj1 = INDIVIDUAL_WEBPAGESS1.objects.get(uid = cl2)
            #feed_obj = feedback_users.objects.filter(school_name=cards_obj1.SCHOOL_NAME).order_by('rating')
            #fed = list(feed_obj)
            #fed1 =fed[0]
            #print(fed1.rating)
            print(cards_obj)
            return render(request,'affliateslist.html',{'cards_obj':cards})
        else:
            return render(request,'affliatesnotfound.html')
    return render(request,'index1.html')



#notify view when school search is not found to add email and home to database
def notify(request):
    if request.method == "POST" :
        email = request.POST['email']
        phone = request.POST['phone']
        not_obj = notify_users(email = email ,phone= phone )
        not_obj.save()
        return render(request,'affliatesnotfound.html')


    
def rough2(request):
    return render(request,'rough2.html')    

'''
class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        data = {
             'today': datetime.date.today(), 
             'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
        }
        pdf = render_to_pdf('pdf/invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

'''
def GeneratePdf(request):
    data = {
            'today': datetime.date.today(), 
            'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
        }
    return render (request,'pdf/invoice.html',data)    

def create_pdf(request):
    data = {
            'today': datetime.date.today(), 
            'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
    }
    pdf = render_to_pdf('transcripts.html',data)
    return HttpResponse(pdf, content_type='application/pdf')

    

'''
def GeneratePDF(request):
    context = {
            "invoice_id": 123,
            "customer_name": "John Cooper",
            "amount": 1399.99,
            "today": "Today",
        }
    # = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")    '''   


'''
class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('invoice.html')
        context = {
            "invoice_id": 123,
            "customer_name": "John Cooper",
            "amount": 1399.99,
            "today": "Today",
        }
        html = template.render(context)
        pdf = render_to_pdf('invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")     
   
'''
def school_template(request):
    return render(request,"geekzmicroschoolvelachery.html")


def rough(request):
    labels = []
    data = []
    queryset = City.objects.order_by('-population')[:5]
    for city in queryset:
        labels.append(city.name)
        data.append(city.population)

    return render(request, 'rough.html', {
        'labels': labels,
        'data': data,
    })


def bulk_load(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    uid_obj = USER_DETAILS.objects.get(USER_EMAIL=user.email)
    #photos_list = Photo_webpage1.objects.filter(gala_admin = uid_obj.uid) 
    #print('h',photos_list)
    print('hello')
    #print(items)
    if request.method == "POST" :
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            user_id=request.session['user_id']
            user=User.objects.get(id=user_id)
            uid_obj = USER_DETAILS.objects.get(USER_EMAIL=user.email)
            g_obj = INDIVIDUAL_WEBPAGESS1.objects.filter(uid = uid_obj.uid)
            g_obj = list(g_obj)
            g_obj = g_obj[0]
            print('hiiiii')
            ## image compression function 
            def OptimizePics(f):
                try:
                    name = str(f).split('.')[0]
                    image = Image.open(f)
                    image.thumbnail((1500, 1500), Image.ANTIALIAS)
                    thumbnail = BytesIO()
                    # Default quality is quality=75
                    image.save(thumbnail, format='JPEG', quality=80)
                    thumbnail.seek(0)
                    newImage = InMemoryUploadedFile(thumbnail,
                                            None,
                                            name + ".jpg",
                                            'image/jpeg',
                                            thumbnail.tell(),
                                            None)
                    return newImage
                except Exception as e:
                    return e
            g_file1 = request.FILES['file']
           # g_file =  OptimizePics(g_file1) # saving the new image file in new variable
            photo_obj = Photo_webpage1(gala_admin=g_obj,file= g_file1)
            photo_obj.save()
            complete_FLAG = INDIVIDUAL_WEBPAGESS1.objects.get(uid = uid_obj.uid)
            complete_FLAG.IS_COMPLETE = "Y"
            complete_FLAG.save(update_fields=['IS_COMPLETE'])
            photo = Photo_webpage1.objects.get(file=g_file1)

            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
            #photos_list = Photo_webpage1.objects.all()  
        else:
            data = {'is_valid': False}
           # photos_list = Photo_webpage1.objects.all()
        return JsonResponse(data)
    
    return render(request,'bulk_load.html') 

'''def drag_load(request):
    photos_list = Photo_webpage.objects.all()
    if request.method == "POST" :
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
            photos_list = Photo_webpage.objects.all()
        else:
            data = {'is_valid': False}
            photos_list = Photo_webpage.objects.all()
        print(photos_list)   
        return JsonResponse(data)
    return render(request,'drag_load.html',{'photos': photos_list}) '''
    
def clear_database(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    uid_obj = USER_DETAILS.objects.get(USER_EMAIL=user.email)
    for photo in Photo_webpage1.objects.filter(gala_admin = uid_obj.uid):
        photo.file.delete()
        photo.delete()
    return redirect(request.POST.get('next'))


def affliateslist(request):
    return render(request,'affliateslist.html')

def affliates_List(request):
    return render(request,'affliates_List.html')    

def affliates_form(request):
    if request.method == "POST" :
        SaaSLoc_lat=float(request.POST['loc_lat'])
        SaaSLoc_long=float(request.POST['loc_long'])
        user_location = Point(SaaSLoc_long,SaaSLoc_lat)
        cr = MICRO_APPLY.objects.values()
        clients = cr.filter(location__distance_lt=(user_location,Distance(m=5000)))
        print(type(clients))
        print(clients)
        cl = list(clients)
        print('hhhhhhhhhhhhhhhhhhhh',cl)
        if clients:
            cl1 = cl[0]
            cl2 = cl1['uid']
            print(cl2)
            cards_obj = INDIVIDUAL_WEBPAGESS1.objects.filter(uid = cl2)
            print(cards_obj)
            return render(request,'affliateslist.html',{'clients_within_radius':clients,'cards_obj':cards_obj})
        else:
            return render(request,'affliatesnotfound.html')        


def feedback_form(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    SCHOOL_NAME = request.GET.get('SCHOOL_NAME')
    school_names = INDIVIDUAL_WEBPAGESS1.objects.all().values('SCHOOL_NAME').distinct()
    if request.method == "POST" :
        user_id=request.session['user_id']
        user=User.objects.get(id=user_id)
        ud = user.id
        name = request.POST['name']
        review = request.POST['review']
        rating = request.POST['rating']
        school_names = INDIVIDUAL_WEBPAGESS1.objects.all().values('SCHOOL_NAME').distinct()
        schools = request.POST['schools']
        OBJ = INDIVIDUAL_WEBPAGESS1.objects.filter(SCHOOL_NAME=schools)
        obj = list(OBJ)
        obj = obj[0]
        obj, created = feedback_user.objects.update_or_create(user_id=ud,defaults={"name":name,"feedback":review,"rating":rating,"SCHOOL":schools,"school_name":obj})
        return render(request,'feedback_form.html')
    return render(request,'feedback_form.html',{'school_name':school_names})   

@login_required
def student_apply(request,SCHOOL_NAME):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    print(user.id)
    student = studentApplications.objects.filter(student_id=user.id)
    if student:
        return redirect('student_profiling')
    else:
        obj = academicYear.objects.all()
        if request.method == "POST" :
            print('hi')
            print(SCHOOL_NAME)
            user_id=request.session['user_id']
            user=User.objects.get(id=user_id)
            print(user.id)
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            gender = request.POST['gender']
            SaaSDOB = request.POST['SaaSDOB']
            enrolling_grade = request.POST['enrolling_grade']
            enrolling_term = request.POST['enrolling_term']
            academic = request.POST['academic']
            attendedschool = request.POST['attendedschool']
            Fathersname = request.POST['Fathersname']
            Fathersoccupation = request.POST['Fathersoccupation']
            Mothersname = request.POST['Mothersname']
            Mothersoccupation = request.POST['Mothersoccupation']
            income = request.POST['income']
            address = request.POST['address']
            email = request.POST['email']
            number = request.POST['number']
            geekzcommute = request.POST['geekzcommute']
            yescommutelocation = request.POST['yescommutelocation']
            childproud = request.POST['childproud']
            familyactivities = request.POST['familyactivities']
            childsinterests = request.POST['childsinterests']
            yourdreams = request.POST['yourdreams']
            medicalcondition = request.POST['medicalcondition']
            childsuspended = request.POST['childsuspended']
            anythingelse = request.POST['anythingelse']
            hear_about = request.POST['hear_about']
            micro_web = INDIVIDUAL_WEBPAGESS1.objects.filter(SCHOOL_NAME=SCHOOL_NAME)
            micro_web1 = list(micro_web)
            micro_web1 = micro_web1[0]
            application_obj = studentApplications(email=email,phone= number,academic_year=academic,enrolling_term=enrolling_term,enrolling_grade=enrolling_grade,first_name=first_name,last_name=last_name,gender=gender,SaaSDOB=SaaSDOB,attendedschool=attendedschool,Fathersname=Fathersname,Fathersoccupation=Fathersoccupation,Mothersname=Mothersname,Mothersoccupation=Mothersoccupation,income=income,address=address,geekzcommute=geekzcommute,yescommutelocation=yescommutelocation,childproud=childproud,familyactivities=familyactivities,childsinterests=childsinterests,yourdreams=yourdreams,medicalcondition=medicalcondition,childsuspended=childsuspended,anythingelse=anythingelse,hear_about=hear_about,IS_COMPLETE='Y',student_id=user.id,microschool= micro_web1)
            application_obj.save()
            student = studentApplications.objects.get(student_id = user.id)
            form = IndividualSlotCreationForm()
            subject='Application submitted'
            html_template='socialaccount/email/student_application.html'
            html_message=render_to_string(html_template,{'microschool': student.microschool.SCHOOL_NAME})
            to_email= student.email
            message=EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [to_email])
            message.content_subtype='html'
            message.send()
            return redirect('student_profiling')
    return render(request,'student_apply.html',{'obj':obj}) 

def student_profiling(request): 
    form = IndividualSlotCreationForm()
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    student_obj = studentApplications.objects.get(student_id = user.id)
    event_obj = StudentProfilings.objects.filter(uid=student_obj)
    if event_obj:
        objs = StudentProfilings.objects.get(uid=student_obj)
        return render(request,'studentreschedule.html',{'heading':objs.HEADING})
    else:
        if request.method == 'POST':
            print("inside  profiling")
            form = IndividualSlotCreationForm(request.POST)
            if form.is_valid():
                schedule_date = form.cleaned_data['schedule_date']
                slot = form.cleaned_data['slot']
                modeofprofiling = form.cleaned_data['modeofprofiling']
                user_id=request.session['user_id']
                user=User.objects.get(id=user_id)
                slot_obj = Individual_admin_slots.objects.filter(id=slot.id)
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
                start = datetime.datetime.strptime(qq.slot, '%I:%M %p')
                end = start + datetime.timedelta(minutes=float(nn))
                start = start.strftime("%I:%M %p")
                end = end.strftime("%I:%M %p")
                start_time = date_obj + " "+ start_time 
                start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %I:%M %p')
                end_time = start_time + datetime.timedelta(minutes=float(nn))
                start_time = start_time.astimezone(timezone('Asia/Kolkata')) # time zone attached
                end_time = end_time.astimezone(timezone('Asia/Kolkata'))   # time zone attached
                print('st',start)
                print('et', end_time)
                print("type",type(start_time))
                heading = qq.day + " " + datee + " " + "at" + " " + start + " " + "to" + " " + end
                service_account_email = "geekzcalendar@geekzcaldendar.iam.gserviceaccount.com"
                SCOPES = ["https://www.googleapis.com/auth/calendar"]
                credentials = ServiceAccountCredentials.from_json_keyfile_name( filename="clientsecret_geekz.json", scopes=SCOPES )
                def build_service():
                    service = build("calendar", "v3", credentials=credentials)
                    return service
                    
                def create_event():
                    service = build_service()
                    event_cal = (service.events().insert(calendarId="thkmk74n50mn6kt14hi1qdru58@group.calendar.google.com",body={
                    "summary": "GEEKZ",
                    "description": "GEEKZ INTERVIEW FOR STUDENT ADMISSION",
                    "start":{"dateTime":start_time.isoformat()}, 
                    "end": {
                        "dateTime": end_time.isoformat()
                            },
                    "reminders": {"useDefault": True},
                    "attendees":user.email,

                        }).execute())     
                    print("ee",event_cal) 
                    student_obj = studentApplications.objects.filter(student_id=user.id)
                    s = list(student_obj)
                    s = s[0]
                    emailObject = MICRO_APPLY.objects.get(uid = s.microschool.uid)
                    #create_event.link = event_cal['hangoutLink'] ##  fetch google meet link from event_cal 
                    profiling_obj = StudentProfilings(uid =s, IS_PROFILINGCOMPLETE='Y',USER = s.microschool.SCHOOL_NAME , EVENT_ID = event_cal['id'],ICalUID=event_cal['iCalUID'],START_TIME= event_cal['start']['dateTime'],END_TIME = event_cal['end']['dateTime'],HEADING= heading,slot= qq,schedule_date= schedule_date,modeofprofiling=modeofprofiling)
                    profiling_obj.save()
                    subject='Student Profiling Confirmation'
                    html_template='socialaccount/email/studentprofilingconfirmation.html'
                    html_message=render_to_string(html_template,{'heading':heading,'id':s.student_id})
                    to_email= user.email
                    message=EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [to_email])
                    message.content_subtype='html' 
                    message.send()
                    ##### email to admin
                    subject='Student Profiling Confirmation to admin'
                    html_template='socialaccount/email/studentprofilingconfirmationtoadmin.html'
                    html_message=render_to_string(html_template,{'heading':heading,'email':s.email})
                    to_email=  emailObject.EMAIL
                    message=EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [to_email])
                    message.content_subtype='html' 
                    message.send()
                create_event()
                student_obj = studentApplications.objects.get(student_id=user.id)
                student_obj.Profiling_scheduled ='Y'
                student_obj.save(update_fields=['Profiling_scheduled'])
                #location = INDIVIDUAL_WEBPAGESS1.objects.get(SCHOOL_NAME=student_obj.microschool.SCHOOL_NAME)
                return render(request,'studentreschedule.html',{'heading':heading})
    return render(request,'student_profiling.html',{'form':form})  

def studentdeletevent(request):
    if request.method == "POST" :
        user_id=request.session['user_id']
        user=User.objects.get(id=user_id)
        student_obj = studentApplications.objects.get(student_id = user.id)
        event_obj = StudentProfilings.objects.get(uid=student_obj)
        SaaSreason=request.POST['reason']
        reason_ob = RESCHEDULE_REASON(uid = user.id,reason=SaaSreason)
        reason_ob.save()
        emailObject = MICRO_APPLY.objects.get(uid = student_obj.microschool.uid)
        subject='Student Profiling Rescheduled by student'
        html_template='socialaccount/email/reschedulebystudent.html'
        html_message=render_to_string(html_template,{'heading':event_obj.HEADING})
        to_email= emailObject.EMAIL
        message=EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [to_email])
        message.content_subtype='html' 
        message.send()
        service_account_email = "geekzcalendar@geekzcaldendar.iam.gserviceaccount.com"
        SCOPES = ["https://www.googleapis.com/auth/calendar"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name( filename="clientsecret_geekz.json", scopes=SCOPES )
        def build_service():
            service = build("calendar", "v3", credentials=credentials)
            return service
                        
        def create_event():
            service = build_service()
            event_cal = (service.events().delete(calendarId="thkmk74n50mn6kt14hi1qdru58@group.calendar.google.com",eventId = event_obj.EVENT_ID).execute() )     
        create_event()
        StudentProfilings.objects.filter(uid =student_obj ).delete()
        form = SlotCreationForm()
        return render(request,"student_profiling.html",{'form': form})

def individualAdminSlotsView(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    uid_obj = USER_DETAILS.objects.get(USER_EMAIL=user.email)
    Iw = INDIVIDUAL_WEBPAGESS1.objects.filter(uid = uid_obj.uid)
    Iw1 = list(Iw)
    Iw1 = Iw1[0]
    ias = Individual_admin_slots.objects.filter(admin_id = Iw1)
    slots_monday =Individual_admin_slots.objects.filter(admin_id = Iw1, day='Monday')
    slots_tuesday = Individual_admin_slots.objects.filter(admin_id = Iw1, day='Tuesday') 
    slots_wednesday = Individual_admin_slots.objects.filter(admin_id = Iw1, day='Wednesday')
    slots_thursday = Individual_admin_slots.objects.filter(admin_id = Iw1, day='Thursday')
    slots_friday = Individual_admin_slots.objects.filter(admin_id = Iw1, day='Friday')
    slots_saturday = Individual_admin_slots.objects.filter(admin_id = Iw1, day='Saturday')
    return render(request,'individualAdminDashboard/individualAdminSlotsView.html',{'slots_monday':slots_monday,'slots_tuesday':slots_tuesday,'slots_wednesday':slots_wednesday,'slots_thursday':slots_thursday,'slots_friday':slots_friday,'slots_saturday':slots_saturday,'ias': ias})


def individualAdminSlots(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    uid_obj = USER_DETAILS.objects.get(USER_EMAIL=user.email)
    profile = MICRO_APPLY.objects.filter(uid = uid_obj.uid)
    if request.method == "POST" :
        user_id=request.session['user_id']
        user=User.objects.get(id=user_id)
        uid_obj = USER_DETAILS.objects.get(USER_EMAIL=user.email)
        profile = MICRO_APPLY.objects.filter(uid = uid_obj.uid)
        admin_id = INDIVIDUAL_WEBPAGESS1.objects.filter(uid= uid_obj.uid)
        admin_id = list(admin_id)
        admin_id = admin_id[0]
        time_duration = float(request.POST['duration'])
        start_time = request.POST['Start-time']
        end_time = request.POST['End-time']
        day = request.POST['Days']
        start_datetime_object =  datetime.datetime.strptime(start_time, '%H:%M')
        end_datetime_object =  datetime.datetime.strptime(end_time, '%H:%M')
        start_datetime_object = start_datetime_object.strftime("%I:%M %p")
        end_datetime_object = end_datetime_object.strftime("%I:%M %p")
        start_datetime_object =  datetime.datetime.strptime(start_datetime_object, '%I:%M %p')
        end_datetime_object =  datetime.datetime.strptime(end_datetime_object, '%I:%M %p')
        msg = ''
        def time_slots(start_datetime_object, end_datetime_object,duration):
            t = start_datetime_object
            while t < end_datetime_object:
                yield t.strftime('%I:%M %p')
                ss = Individual_admin_slots.objects.filter(admin_id= admin_id,slot= t.strftime('%I:%M %p'),day=day)
                if not ss:
                    slot_obj = Individual_admin_slots(slot=t.strftime('%I:%M %p'),day=day,duration=time_duration,admin_id=admin_id)
                    t += datetime.timedelta(minutes=time_duration)
                    slot_obj.save()
                    print(t.strftime('%I:%M %p'))
                else:
                    pass
                     
        print(list(time_slots(start_datetime_object, end_datetime_object,time_duration)))
        return render(request,'individualAdminDashboard/individualAdminSlots.html',{'profile':profile})
    return render(request,'individualAdminDashboard/individualAdminSlots.html',{'profile':profile})



def edit_time_slot(request,pk):
    ob = Individual_admin_slots.objects.get(pk=pk)
    obj = Individual_admin_slots.objects.filter(pk=pk)
    day = ob.day
    if request.method == "POST" :
        inform_student = Individual_admin_slots.objects.get(day = day)
        st = StudentProfilings.objects.get(slot=inform_student)
        student = st.uid.email
        subject='Student  Profiling Reschedule'
        html_template='socialaccount/email/student_profiling_reschedule.html'
        html_message=render_to_string(html_template)
        to_email= student
        message=EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [to_email])
        message.content_subtype='html' 
        message.send()
        service_account_email = "geekzcalendar@geekzcaldendar.iam.gserviceaccount.com"
        SCOPES = ["https://www.googleapis.com/auth/calendar"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name( filename="clientsecret_geekz.json", scopes=SCOPES )
        def build_service():
            service = build("calendar", "v3", credentials=credentials)
            return service
                        
        def create_event():
            service = build_service()
            event_cal = (service.events().delete(calendarId="thkmk74n50mn6kt14hi1qdru58@group.calendar.google.com",eventId = st.EVENT_ID).execute() )     
        create_event()
        ob1 = Individual_admin_slots.objects.filter(day = day).delete()
        user_id=request.session['user_id']
        user=User.objects.get(id=user_id)
        uid_obj = USER_DETAILS.objects.get(USER_EMAIL=user.email)
        profile = MICRO_APPLY.objects.filter(uid = uid_obj.uid)
        admin_id = INDIVIDUAL_WEBPAGESS1.objects.filter(uid= uid_obj.uid)
        admin_id = list(admin_id)
        admin_id = admin_id[0]
        time_duration = float(request.POST['duration'])
        start_time = request.POST['Start-time']
        end_time = request.POST['End-time']
        day = request.POST['day']
        start_datetime_object =  datetime.datetime.strptime(start_time, '%H:%M')
        end_datetime_object =  datetime.datetime.strptime(end_time, '%H:%M')
        start_datetime_object = start_datetime_object.strftime("%I:%M %p")
        end_datetime_object = end_datetime_object.strftime("%I:%M %p")
        start_datetime_object =  datetime.datetime.strptime(start_datetime_object, '%I:%M %p')
        end_datetime_object =  datetime.datetime.strptime(end_datetime_object, '%I:%M %p')
        def time_slots(start_datetime_object, end_datetime_object,duration):
            t = start_datetime_object
            while t < end_datetime_object:
                yield t.strftime('%I:%M %p')
                ss = Individual_admin_slots.objects.filter(admin_id= uid_obj.uid,slot= t.strftime('%I:%M %p'),day=day)
                if not ss:
                    slot_obj = Individual_admin_slots(slot=t.strftime('%I:%M %p'),day=day,duration=time_duration,admin_id=admin_id)
                    t += datetime.timedelta(minutes=time_duration)
                    slot_obj.save()
                    print(t.strftime('%I:%M %p'))
                else:
                    msg = 'The slot already exist' 
        print(list(time_slots(start_datetime_object, end_datetime_object,time_duration)))
        return redirect('individualAdminSlotsView')
    return render(request,'individualAdminDashboard/edit_time_slot.html',{'ob':obj})



 ###########################################3   



def superAdmin_slots(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    name = user.first_name
    if request.method == "POST" :
        user_id=request.session['user_id']
        user=User.objects.get(id=user_id)
        time_duration = float(request.POST['duration'])
        start_time = request.POST['Start-time']
        end_time = request.POST['End-time']
        day = request.POST['Days']
        start_datetime_object =  datetime.datetime.strptime(start_time, '%H:%M')
        end_datetime_object =  datetime.datetime.strptime(end_time, '%H:%M')
        start_datetime_object = start_datetime_object.strftime("%I:%M %p")
        end_datetime_object = end_datetime_object.strftime("%I:%M %p")
        start_datetime_object =  datetime.datetime.strptime(start_datetime_object, '%I:%M %p')
        end_datetime_object =  datetime.datetime.strptime(end_datetime_object, '%I:%M %p')
        msg = ''
        def time_slots(start_datetime_object, end_datetime_object,duration):
            t = start_datetime_object
            while t < end_datetime_object:
                yield t.strftime('%I:%M %p')
                ss = SLOTS_DAY.objects.filter(admin= user.id,slot= t.strftime('%I:%M %p'),day=day)
                if not ss:
                    slot_obj = SLOTS_DAY(slot=t.strftime('%I:%M %p'),day=day,duration=time_duration,admin=user.id)
                    t += datetime.timedelta(minutes=time_duration)
                    slot_obj.save()
                    print(t.strftime('%I:%M %p'))
                else:
                    pass
                     
        print(list(time_slots(start_datetime_object, end_datetime_object,time_duration)))
        return render(request,'superAdminDashboard/superAdmin_slots.html',{'name':name})
    return render(request,'superAdminDashboard/superAdmin_slots.html',{'name':name})

def SuperAdminSlotsView(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    name = user.first_name
    ias = SLOTS_DAY.objects.filter(admin = user.id)
    slots_monday =SLOTS_DAY.objects.filter(admin = user.id, day='Monday')
    slots_tuesday = SLOTS_DAY.objects.filter(admin = user.id, day='Tuesday') 
    slots_wednesday = SLOTS_DAY.objects.filter(admin = user.id, day='Wednesday')
    slots_thursday = SLOTS_DAY.objects.filter(admin = user.id, day='Thursday')
    slots_friday = SLOTS_DAY.objects.filter(admin = user.id, day='Friday')
    slots_saturday = SLOTS_DAY.objects.filter(admin =user.id, day='Saturday')
    return render(request,'superAdminDashboard/SuperAdminSlotsView.html',{'slots_monday':slots_monday,'slots_tuesday':slots_tuesday,'slots_wednesday':slots_wednesday,'slots_thursday':slots_thursday,'slots_friday':slots_friday,'slots_saturday':slots_saturday,'ias': ias})

def superedit_time_slot(request,pk):
    ob = SLOTS_DAY.objects.get(pk=pk)
    obj = SLOTS_DAY.objects.filter(pk=pk)
    day = ob.day
    if request.method == "POST" :
        affliate_inform = SLOTS_DAY.objects.filter(day = day)
        affliate_inform = list(affliate_inform)
        affliate_inform = affliate_inform[0]
        email_ob = MICRO_PROFILING.objects.get(slot = affliate_inform )
        email = email_ob.USER
        subject='SaaS  Profiling Reschedule'
        html_template='socialaccount/email/saasprofiling_reschedule.html'
        html_message=render_to_string(html_template)
        to_email= email
        message=EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [to_email])
        message.content_subtype='html' 
        message.send()
        service_account_email = "geekzcalendar@geekzcaldendar.iam.gserviceaccount.com"
        SCOPES = ["https://www.googleapis.com/auth/calendar"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name( filename="clientsecret_geekz.json", scopes=SCOPES )
        def build_service():
            service = build("calendar", "v3", credentials=credentials)
            return service
                        
        def create_event():
            service = build_service()
            event_cal = (service.events().delete(calendarId="thkmk74n50mn6kt14hi1qdru58@group.calendar.google.com",eventId = email_ob.EVENT_ID).execute() )     
        create_event()
        ob1 = SLOTS_DAY.objects.filter(day = day).delete()
        user_id=request.session['user_id']
        user=User.objects.get(id=user_id)
        time_duration = float(request.POST['duration'])
        start_time = request.POST['Start-time']
        end_time = request.POST['End-time']
        day = request.POST['day']
        start_datetime_object =  datetime.datetime.strptime(start_time, '%H:%M')
        end_datetime_object =  datetime.datetime.strptime(end_time, '%H:%M')
        start_datetime_object = start_datetime_object.strftime("%I:%M %p")
        end_datetime_object = end_datetime_object.strftime("%I:%M %p")
        start_datetime_object =  datetime.datetime.strptime(start_datetime_object, '%I:%M %p')
        end_datetime_object =  datetime.datetime.strptime(end_datetime_object, '%I:%M %p')
        def time_slots(start_datetime_object, end_datetime_object,duration):
            t = start_datetime_object
            while t < end_datetime_object:
                yield t.strftime('%I:%M %p')
                ss = SLOTS_DAY.objects.filter(admin= user.id,slot= t.strftime('%I:%M %p'),day=day)
                if not ss:
                    slot_obj = SLOTS_DAY(slot=t.strftime('%I:%M %p'),day=day,duration=time_duration,admin=user.id)
                    t += datetime.timedelta(minutes=time_duration)
                    slot_obj.save()
                    print(t.strftime('%I:%M %p'))
                else:
                    msg = 'The slot already exist' 
        print(list(time_slots(start_datetime_object, end_datetime_object,time_duration)))
        return redirect('SuperAdminSlotsView')
    return render(request,'superAdminDashboard/superedit_time_slot.html',{'ob':obj})

 

def feedetailsreview(request,uid):
    obj = INDIVIDUAL_WEBPAGESS1.objects.filter(uid = uid)
    obj = list(obj)
    obj = obj[0]
    objj = individual_feedetail.objects.filter(admin = obj)
    obj1 = list(objj)
    obj1 = obj1[0]
    affliates = AffliatesfeeStructure.objects.filter(uid=uid,IS_FEEREVIEW_COMPLETE='N')
    affliates1 = AffliatesfeeStructure.objects.filter(uid=uid,IS_FEEREVIEW_COMPLETE='Y')
    if affliates:
        return redirect('feeSplit',uid=uid)
    elif affliates1:
        return redirect('webpage_Approve')
    else:
        if request.method == "POST" :
            fullYear_kindergarten = request.POST['fullYear_kindergarten']
            TaxfullYear_kindergarten = request.POST['TaxfullYear_kindergarten']
            val = float(fullYear_kindergarten) * float(TaxfullYear_kindergarten)
            print(val)
            val = val/100
            print(val)
            total_fullYear_kindergarten = float(fullYear_kindergarten) + val
            print(total_fullYear_kindergarten)
            fall_kindergarten = request.POST['fall_kindergarten']
            Taxfall_kindergarten = request.POST['Taxfall_kindergarten']
            val1 = float(fall_kindergarten) * float(Taxfall_kindergarten)
            print(val1)
            val1 = val1/100
            print(val1)
            total_fall_kindergarten = float(fall_kindergarten) + val1 
            spring_kindergarten = request.POST['spring_kindergarten']
            Taxspring_kindergarten = request.POST['Taxspring_kindergarten']
            val2 = float(spring_kindergarten) * float(Taxspring_kindergarten)
            print(val2)
            val2 = val2/100
            print(val2)
            total_spring_kindergarten = float(spring_kindergarten) + val2 
            fullYear_lowerElementary = request.POST['fullYear_lowerElementary']
            TaxfullYear_lowerElementary = request.POST['TaxfullYear_lowerElementary']
            val3 = float(fullYear_lowerElementary) * float(TaxfullYear_lowerElementary)
            print(val3)
            val3 = val3/100
            print(val3)
            total_fullYear_lowerElementary = float(fullYear_lowerElementary) + val3
            fall_lowerElementary = request.POST['fall_lowerElementary']
            Taxfall_lowerElementary = request.POST['Taxfall_lowerElementary']
            val4 = float(fall_lowerElementary) * float(Taxfall_lowerElementary)
            print(val4)
            val4 = val4/100
            print(val4)
            total_fall_lowerElementary = float(fall_lowerElementary) + val4
            spring_lowerElementary = request.POST['spring_lowerElementary']
            Taxspring_lowerElementary = request.POST['Taxspring_lowerElementary']
            val5 = float(spring_lowerElementary) * float(Taxspring_lowerElementary)
            print(val5)
            val5 = val5/100
            print(val5)
            total_spring_lowerElementary = float(spring_lowerElementary) + val5
            fullYear_UpperElementary = request.POST['fullYear_UpperElementary']
            TaxfullYear_UpperElementary = request.POST['TaxfullYear_UpperElementary']
            val6 = float(fullYear_UpperElementary) * float(TaxfullYear_UpperElementary)
            print(val6)
            val6 = val6/100
            print(val6)
            total_fullYear_UpperElementary= float(fullYear_UpperElementary) + val6
            fall_UpperElementary = request.POST['fall_UpperElementary']
            Taxfall_UpperElementary = request.POST['Taxfall_UpperElementary']
            val7 = float(fall_UpperElementary) * float(Taxfall_UpperElementary)
            print(val7)
            val7 = val7/100
            print(val7)
            total_fall_UpperElementary= float(fall_UpperElementary) + val7
            spring_UpperElementary = request.POST['spring_UpperElementary']
            Taxspring_UpperElementary = request.POST['Taxspring_UpperElementary']
            val8 = float(spring_UpperElementary) * float(Taxspring_UpperElementary)
            print(val8)
            val8 = val8/100
            print(val8)
            total_spring_UpperElementary= float(spring_UpperElementary) + val8 
            aff = AffliatesfeeStructure(uid = uid,school = obj1,TaxfullYear_kindergarten = TaxfullYear_kindergarten,total_fullYear_kindergarten=total_fullYear_kindergarten,Taxfall_kindergarten=Taxfall_kindergarten,total_fall_kindergarten=total_fall_kindergarten,Taxspring_kindergarten=Taxspring_kindergarten,total_spring_kindergarten=total_spring_kindergarten,TaxfullYear_lowerElementary=TaxfullYear_lowerElementary,total_fullYear_lowerElementary=total_fullYear_lowerElementary,Taxfall_lowerElementary=Taxfall_lowerElementary,total_fall_lowerElementary=total_fall_lowerElementary,Taxspring_lowerElementary=Taxspring_lowerElementary,total_spring_lowerElementary=total_spring_lowerElementary,TaxfullYear_UpperElementary=TaxfullYear_UpperElementary,total_fullYear_UpperElementary=total_fullYear_UpperElementary,Taxfall_UpperElementary=Taxfall_UpperElementary,total_fall_UpperElementary=total_fall_UpperElementary,Taxspring_UpperElementary=Taxspring_UpperElementary,total_spring_UpperElementary=total_spring_UpperElementary)
            aff.save()
            return redirect('feeSplit',uid=uid) 
    return render(request,'superAdminDashboard/feedetailsreview.html',{'objj':objj})
    #return render(request,'superAdminDashboard/feedetailsreview.html')

def feeSplit(request,uid):
    ob = AffliatesfeeStructure.objects.filter(uid=uid)
    if request.method == "POST" :
        split1_fullYear_kindergarten = request.POST['split1_fullYear_kindergarten']
        split2_fullYear_kindergarten = request.POST['split2_fullYear_kindergarten']
        split3_fullYear_kindergarten = request.POST['split3_fullYear_kindergarten']
        split1_fall_kindergarten = request.POST['split1_fall_kindergarten']
        split2_fall_kindergarten = request.POST['split2_fall_kindergarten']
        split1_spring_kindergarten = request.POST['split1_spring_kindergarten']
        split1_fullYear_lowerElementary = request.POST['split1_fullYear_lowerElementary']
        split2_fullYear_lowerElementary = request.POST['split2_fullYear_lowerElementary']
        split3_fullYear_lowerElementary = request.POST['split3_fullYear_lowerElementary']
        split1_fall_lowerElementary = request.POST['split1_fall_lowerElementary']
        split2_fall_lowerElementary = request.POST['split2_fall_lowerElementary']
        split1_spring_lowerElementary = request.POST['split1_spring_lowerElementary']
        split1_fullYear_UpperElementary = request.POST['split1_fullYear_UpperElementary']
        split2_fullYear_UpperElementary = request.POST['split2_fullYear_UpperElementary']
        split3_fullYear_UpperElementary = request.POST['split3_fullYear_UpperElementary']
        split1_fall_UpperElementary = request.POST['split1_fall_UpperElementary']
        split2_fall_UpperElementary = request.POST['split2_fall_UpperElementary']
        split1_spring_UpperElementary = request.POST['split1_spring_UpperElementary']
        termfees = AffliatesfeeStructure.objects.get(uid=uid)
        termfees.split1_fullYear_kindergarten=split1_fullYear_kindergarten
        termfees.split2_fullYear_kindergarten = split2_fullYear_kindergarten
        termfees.split3_fullYear_kindergarten = split3_fullYear_kindergarten
        termfees.split1_fall_kindergarten = split1_fall_kindergarten
        termfees.split2_fall_kindergarten = split2_fall_kindergarten
        termfees.split1_spring_kindergarten = split1_spring_kindergarten
        termfees.split1_fullYear_lowerElementary = split1_fullYear_lowerElementary
        termfees.split2_fullYear_lowerElementary = split2_fullYear_lowerElementary
        termfees.split3_fullYear_lowerElementary = split3_fullYear_lowerElementary
        termfees.split1_fall_lowerElementary = split1_fall_lowerElementary
        termfees.split2_fall_lowerElementary = split2_fall_lowerElementary
        termfees.split1_spring_lowerElementary = split1_spring_lowerElementary
        termfees.split1_fullYear_UpperElementary = split1_fullYear_UpperElementary
        termfees.split2_fullYear_UpperElementary = split2_fullYear_UpperElementary
        termfees.split3_fullYear_UpperElementary = split3_fullYear_UpperElementary
        termfees.split1_fall_UpperElementary = split1_fall_UpperElementary
        termfees.split2_fall_UpperElementary = split2_fall_UpperElementary
        termfees.split1_spring_UpperElementary = split1_spring_UpperElementary
        termfees.save(update_fields=['split1_fullYear_kindergarten','split2_fullYear_kindergarten','split3_fullYear_kindergarten','split1_fall_kindergarten','split2_fall_kindergarten','split1_spring_kindergarten','split1_fullYear_lowerElementary','split2_fullYear_lowerElementary','split3_fullYear_lowerElementary','split1_fall_lowerElementary','split2_fall_lowerElementary','split1_spring_lowerElementary','split1_fullYear_UpperElementary','split2_fullYear_UpperElementary','split3_fullYear_UpperElementary','split1_fall_UpperElementary','split2_fall_UpperElementary','split1_spring_UpperElementary'])
        complete = AffliatesfeeStructure.objects.get(uid = uid)
        complete.IS_FEEREVIEW_COMPLETE = 'Y'
        complete.save(update_fields=['IS_FEEREVIEW_COMPLETE'])
        return redirect('webpage_Approve')
    return render(request,'superAdminDashboard/feeSplit.html',{'ob':ob})

def INDIVIDUAL_WEBPAGESSApprove(request,uid):
    web_approve = INDIVIDUAL_WEBPAGESS1.objects.get(uid = uid)
    web_approve.IS_APPROVED = "Y"
    web_approve.save(update_fields=['IS_APPROVED'])
    return redirect('webpage_Approve')

def INDIVIDUAL_WEBPAGESSReject(request,uid):
    web_approve = INDIVIDUAL_WEBPAGESS1.objects.get(uid = uid)
    web_approve.IS_APPROVED = "R"
    web_approve.save(update_fields=['IS_APPROVED'])
    return redirect('webpage_Approve')

def addAcademicYear(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    name = user.first_name
    if request.method == "POST" :
        year = request.POST['year']
        id,year = academicYear.objects.update_or_create(uid=user.id,defaults={"academic_year":year})
        return redirect('superAdmin_dashboard')
    return render(request,'superAdminDashboard/addAcademicYear.html',{'name':name})    

def duedatesADD(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    name = user.first_name
    if request.method == "POST":
        Term1_duedate  =  request.POST['Term1_duedate']
        Term2_duedate  =  request.POST['Term2_duedate'] 
        Term3_duedate  =  request.POST['Term3_duedate']
        id,term = duedates.objects.update_or_create(pk=1,defaults={'Term1_duedate':Term1_duedate,'Term2_duedate':Term2_duedate,'Term3_duedate':Term3_duedate})   
        return redirect('superAdmin_dashboard')
    return render(request,'superAdminDashboard/duedatesADD.html',{'name':name})


 # ajax view to get slots and populate in dropdown and reading calendar to filter slots
def individual_load_slots(request):
    print("individual_slot")
    date = request.GET.get('day_id')
    print(date)
    def findDay(date):
        born = datetime.datetime.strptime(date, '%Y-%m-%d').weekday() 
        return (calendar.day_name[born])
    slots = Individual_admin_slots.objects.filter(day=findDay(date)).all()
    return render(request, 'slots_dropdown_list_options.html', {'slots': slots}) 

def invoice(request):
    return render(request,'invoice.html')



def Invoice_requests(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    print(user)
    student_obj = studentApplications.objects.get(student_id=user.id)
    invoice_obj = InvoiceRequest(email= student_obj.email,first_name=student_obj.first_name,last_name=student_obj.last_name,Fathersname=student_obj.Fathersname,address=student_obj.address,microschool=student_obj.microschool.SCHOOL_NAME,student_id=user.id)
    invoice_obj.save()
    print('HIIIIII')
    location = INDIVIDUAL_WEBPAGESS1.objects.get(SCHOOL_NAME=student_obj.microschool.SCHOOL_NAME)
    return redirect('webpage',LOCALITY=location.LOCALITY)

def bsbasicInvoice(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    uid_obj = USER_DETAILS.objects.get(USER_EMAIL=user.email)
    profile = MICRO_APPLY.objects.filter(uid = uid_obj.uid)
    sch = INDIVIDUAL_WEBPAGESS1.objects.get(uid = uid_obj.uid)
    invoice = InvoiceRequest.objects.filter(microschool=sch.SCHOOL_NAME,IS_COMPLETE='N')
    return render(request,'individualAdminDashboard/bs-basicInvoice.html',{'invoice':invoice,'profile':profile})



def transcriptsApprove(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    uid_obj = USER_DETAILS.objects.get(USER_EMAIL=user.email)
    profile = MICRO_APPLY.objects.filter(uid = uid_obj.uid)
    sch = INDIVIDUAL_WEBPAGESS1.objects.get(uid = uid_obj.uid)
    transcripts = transcriptsRequest.objects.filter(microschool=sch.SCHOOL_NAME,IS_COMPLETE='N',payment_complete='Y')
    return render(request,"individualAdminDashboard/transcriptsApprove.html",{'transcripts': transcripts,'profile':profile})


def transcripts_request(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    print(user)
    student_obj = studentApplications.objects.get(student_id=user.id)
    trans_obj = transcriptsRequest(email=student_obj.email,first_name=student_obj.first_name,last_name=student_obj.last_name,Fathersname=student_obj.Fathersname,address=student_obj.address,microschool=student_obj.microschool.SCHOOL_NAME,student_id=user.id,payment_complete='Y')
    trans_obj.save()
    location = INDIVIDUAL_WEBPAGESS1.objects.get(SCHOOL_NAME=student_obj.microschool.SCHOOL_NAME)
    return redirect('webpage',LOCALITY=location.LOCALITY)

def newApplications(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    uid_obj = USER_DETAILS.objects.get(USER_EMAIL=user.email)
    profile = MICRO_APPLY.objects.filter(uid = uid_obj.uid)
    sch = INDIVIDUAL_WEBPAGESS1.objects.filter(uid = uid_obj.uid)
    sch1 = list(sch)
    sch1 = sch1[0]
    student_obj = studentApplications.objects.filter(microschool=sch1)
    return render(request,'individualAdminDashboard/newApplications.html',{'student_obj': student_obj,'profile':profile})

def IndividualApproveProfiling(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    uid_obj = USER_DETAILS.objects.get(USER_EMAIL=user.email)
    profile = MICRO_APPLY.objects.filter(uid = uid_obj.uid)
    ud = INDIVIDUAL_WEBPAGESS1.objects.filter(uid = uid_obj.uid)
    ud1 = list(ud)
    ud1 = ud1[0]
    objectProf = studentProfileFeedback.objects.filter(school=ud1.SCHOOL_NAME, Profiling_done='Y')
    return render(request,'individualAdminDashboard/individualprofiling.html',{'objectProf':objectProf,'profile':profile})

def studentProfilingadmin_Approve(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    name = user.first_name
    objectProf = studentProfileFeedback.objects.filter(Profiling_done='Y')
    return render(request,'superAdminDashboard/studentProfilingadmin_Approve.html',{'objectProf':objectProf,'name':name})

def Studentfeedbackprofiling(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    uid_obj = USER_DETAILS.objects.get(USER_EMAIL=user.email)
    ud = INDIVIDUAL_WEBPAGESS1.objects.get(uid = uid_obj.uid)
    profile = MICRO_APPLY.objects.filter(uid = uid_obj.uid)
    scheduled = StudentProfilings.objects.filter( IS_PROFILINGCOMPLETE='Y',IS_APPROVED='N',USER=ud.SCHOOL_NAME)
    return render(request,'individualAdminDashboard/Studentfeedbackprofiling.html',{'profile':profile,'scheduled':scheduled})

def StudentprofileMessage(request,id):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    uid_obj = USER_DETAILS.objects.get(USER_EMAIL=user.email)
    ud = INDIVIDUAL_WEBPAGESS1.objects.get(uid = uid_obj.uid)
    profile = MICRO_APPLY.objects.filter(uid = uid_obj.uid)
    if request.method == "POST":
        user_id=request.session['user_id']
        user=User.objects.get(id=user_id)
        uid_obj = USER_DETAILS.objects.get(USER_EMAIL=user.email)
        ud = INDIVIDUAL_WEBPAGESS1.objects.get(uid = uid_obj.uid)
        profile = MICRO_APPLY.objects.filter(uid = uid_obj.uid)
        student_obj = studentApplications.objects.get(student_id=id)
        scheduled = StudentProfilings.objects.get( uid = student_obj)
        feedback  =  request.POST['feedback']
        feedback_obj = studentProfileFeedback(uid = id ,feedback=feedback,Profiling_done = 'Y',school=ud.SCHOOL_NAME,studentProfile= scheduled)
        feedback_obj.save()
        student_obj.Profiling_complete = 'Y'
        student_obj.save(update_fields = ['Profiling_complete'])
        return redirect('Studentfeedbackprofiling')
    return render(request,'individualAdminDashboard/StudentprofileMessage.html',{'profile':profile})

def complete_profiling(request,student_id):
    student_obj = studentApplications.objects.get(student_id=student_id)
    student_obj.Profiling_complete ='Y'
    student_obj.save(update_fields=['Profiling_complete'])
    student_objj = studentApplications.objects.filter(student_id=student_id)
    o = list(student_objj)
    o = o[0]
    objectProf = StudentProfilings.objects.filter(uid = o)
    return redirect('IndividualApproveProfiling')

def approve_profiling(request,student_id):
    student_obj = studentApplications.objects.get(student_id=student_id)
    student_obj.Profiling_approved ='Y'
    student_obj.save(update_fields=['Profiling_approved'])
    Prof = StudentProfilings.objects.get(uid = student_obj)
    Prof.IS_APPROVED = 'Y'
    Prof.save(update_fields=['IS_APPROVED'])
    subject='Kid Selected'
    html_template='socialaccount/email/onselectionkid.html'
    html_message=render_to_string(html_template)
    to_email= student_obj.email
    message=EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [to_email])
    message.content_subtype='html' 
    message.send()
    return redirect('IndividualApproveProfiling')

def reject_profiling(request,student_id):
    student_obj = studentApplications.objects.get(student_id=student_id)
    student_obj.Profiling_approved ='R'
    student_obj.save(update_fields=['Profiling_approved'])
    student_objj = studentApplications.objects.filter(student_id=student_id)
    o = list(student_objj)
    o = o[0]
    Prof = StudentProfilings.objects.get(uid = o)
    Prof.IS_APPROVED = 'R'
    Prof.save(update_fields=['IS_APPROVED'])
    objectProf = StudentProfilings.objects.filter(uid = o)
    subject='Kid Selected'
    html_template='socialaccount/email/onrejectionkid.html'
    html_message=render_to_string(html_template)
    to_email= student_obj.email
    message=EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [to_email])
    message.content_subtype='html' 
    message.send()
    return redirect('IndividualApproveProfiling')       

def newenrollments(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    name = user.first_name
    student_tobeEnrolled = studentApplications.objects.filter(Profiling_approved='Y',Enrolled='N') 
    return render(request,'superAdminDashboard/newenrollments.html',{'name':name,'student_tobeEnrolled':student_tobeEnrolled})    

def invoiceConfig(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    name = user.first_name
    schools = INDIVIDUAL_WEBPAGESS1.objects.all()
    if request.method == "POST" :
        school = request.POST['school']
        school_obj = INDIVIDUAL_WEBPAGESS1.objects.get(SCHOOL_NAME = school)
        if school_obj.invoice_generation == 'N':
            return redirect('Enableinvoice',school=school)
        else:
            return redirect('Disableinvoice',school=school)    

    return render(request,'superAdminDashboard/invoiceConfig.html',{'name':name,'schools':schools})

def Enableinvoice(request,school):
    if request.method == "POST" :
        school_obj = INDIVIDUAL_WEBPAGESS1.objects.get(SCHOOL_NAME=school)
        school_obj.invoice_generation = 'Y'
        school_obj.save(update_fields=['invoice_generation'])
        return redirect('invoiceConfig')
    return render(request,'superAdminDashboard/Enableinvoice.html',{'school':school})

def Disableinvoice(request,school):
    if request.method == "POST" :
        school_obj = INDIVIDUAL_WEBPAGESS1.objects.get(SCHOOL_NAME=school)
        school_obj.invoice_generation = 'N'
        school_obj.save(update_fields=['invoice_generation'])
        return redirect('invoiceConfig')
    return render(request,'superAdminDashboard/Disableinvoice.html',{'school':school})

def manualgenerate(request,student_id):
    s_obj = studentApplications.objects.get(student_id=student_id)
    obj_invoice = enrolledStudents.objects.get(student_enrolled=s_obj)
    obj_invoice.invoice_show = 'Y'
    obj_invoice.save(update_fields=['invoice_show'])
    return redirect('studentApplications')

def enrollment(request,student_id):
    student_objj = studentApplications.objects.filter(student_id=student_id)
    o = list(student_objj)
    o = o[0]
    student_obj = studentApplications.objects.get(student_id=student_id)
    student_obj.Enrolled ='Y'
    student_obj.save(update_fields=['Enrolled'])
    print(student_obj.enrolling_grade)
    enrolling_grade = student_obj.enrolling_grade
    enrolling_term = student_obj.enrolling_term
    feedetails = individual_feedetail.objects.get(admin = student_obj.microschool)
    fees = AffliatesfeeStructure.objects.get(school = feedetails)
    print(fees)
    grade =''
    Term1 = ''
    Term2 = ''
    Term3 = ''
    if enrolling_grade == 'Pre-K' or enrolling_grade == 'Jr-K' or enrolling_grade == 'Sr-K':
        grade = "Kindergarten studio"
        if enrolling_term == 'Full Year':
            Term1 = fees.split1_fullYear_kindergarten
            Term2 = fees.split2_fullYear_kindergarten
            Term3 = fees.split3_fullYear_kindergarten
        elif enrolling_term == 'Vijayadasami':
            Term1 = fees.split1_fall_kindergarten
            Term2 = fees.split2_fall_kindergarten
            Term3 = "not valid"
        elif enrolling_term == 'Spring':
            Term1 = fees.split1_spring_kindergarten
            Term2 = "not valid"
            Term3 = "not valid"
    elif enrolling_grade == '1st Grade' or enrolling_grade =='2nd Grade' or enrolling_grade =='3rd Grade':
        grade = 'Lower Elementary Studio'
        if enrolling_term == 'Full Year':
            Term1 = fees.split1_fullYear_lowerElementary 
            Term2 = fees.split2_fullYear_lowerElementary 
            Term3 = fees.split3_fullYear_lowerElementary 
        elif enrolling_term == 'Vijayadasami':
            Term1 = fees.split1_fall_lowerElementary 
            Term2 = fees.split2_fall_lowerElementary 
            Term3 = "not valid"
        elif enrolling_term == 'Spring':
            Term1 = fees.split1_spring_lowerElementary
            Term2 = "not valid"
            Term3 = "not valid"
    elif enrolling_grade == '4th Grade' or enrolling_grade == '5th Grade' :
        grade = 'Upper Elementary Studio'
        if enrolling_term == 'Full Year':
            Term1 = fees.split1_fullYear_UpperElementary
            Term2 = fees.split2_fullYear_UpperElementary 
            Term3 = fees.split3_fullYear_UpperElementary
        elif enrolling_term == 'Vijayadasami':
            Term1 = fees.split1_fall_UpperElementary 
            Term2 = fees.split2_fall_UpperElementary 
            Term3 = "not valid"
        elif enrolling_term == 'Spring':
            Term1 = fees.split1_spring_UpperElementary
            Term2 = "not valid"
            Term3 = "not valid"
    student_tobeEnrolled = studentApplications.objects.filter(student_id=student_id) 
    student_tobeEnrolled = list(student_tobeEnrolled)
    student_tobeEnrolled = student_tobeEnrolled[0]   
    enroll = enrolledStudents(student_enrolled=student_tobeEnrolled,school=student_tobeEnrolled.microschool, active_status='Y',Term1=Term1,Term2=Term2,Term3=Term3,academic_year= student_obj.academic_year,grade=grade,current_grade=enrolling_grade,current_enrolling_term=enrolling_term, Term1flag='Y')    
    enroll.save()
    ### FETCH OLD COUNTER
    invoicecounter_obj = invoicecounter.objects.all()
    invoicecounter_obj = list(invoicecounter_obj)
    invoicecounter_obj = invoicecounter_obj[0]
    #### increment the counter
    invoiceNum = invoicecounter_obj.invoice_value + 1
    ###update the counter in database and assign it to invoice of student
    invoicecounter_obj.invoice_value = invoiceNum
    invoicecounter_obj.save(update_fields=['invoice_value'])
    invoice_obj = enrolledStudents.objects.get(student_enrolled=student_tobeEnrolled)
    Totalfees = int(invoice_obj.Term1)+ int(invoice_obj.Term2 )+ int(invoice_obj.Term3)
    print(Totalfees)
    edTech = int(Totalfees) - 36000
    print(edTech)
    invoice_values = studentInvoice(student_id = invoice_obj ,invoice_no=invoiceNum,Totalfees=Totalfees,edTech=edTech,amountpaid=invoice_obj.Term1,academic_year=invoice_obj.academic_year)
    invoice_values.save()
    return redirect('newenrollments')
        


def studentApplicationsview(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    name = user.first_name
    student_obj = studentApplications.objects.all()
    enrolled = enrolledStudents.objects.all()
    return render(request,'superAdminDashboard/studentApplications.html',{'name':name,'student_obj':student_obj,'enrolled':enrolled})

def studentsdata(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    name = user.first_name
    obj = academicYear.objects.all()
    obj = list(obj)
    obj = obj[0]
    enrolled = enrolledStudents.objects.filter(active_status = 'Y',academic_year=obj.academic_year)
    return render(request,'superAdminDashboard/studentsdata.html',{'name':name,'enrolled':enrolled})


def feepayTerm1(request,student_id):
    obj = academicYear.objects.all()
    obj = list(obj)
    obj = obj[0]
    student_object = studentApplications.objects.get(student_id=student_id)
    fees = enrolledStudents.objects.get(student_enrolled= student_object,academic_year= obj.academic_year)
    fees.Term1flag = 'Y'
    fees.save(update_fields=['Term1flag'])
    invoicecounter_obj = invoicecounter.objects.all()
    invoicecounter_obj = list(invoicecounter_obj)
    invoicecounter_obj = invoicecounter_obj[0]
    #### increment the counter
    invoiceNum = invoicecounter_obj.invoice_value + 1
    #invoice_obj = enrolledStudents.objects.get(student_enrolled=fees)
    Totalfees = int(fees.Term1)+ int(fees.Term2 )+ int(fees.Term3)
    print(Totalfees)
    edTech = int(Totalfees) - 36000
    print(edTech)
    invoice_values = studentInvoice(student_id = fees ,invoice_no=invoiceNum,Totalfees=Totalfees,edTech=edTech,amountpaid=fees.Term1,academic_year=fees.academic_year)
    invoice_values.save() 
    ###update the counter in database and assign it to invoice of student
    invoicecounter_obj.invoice_value = invoiceNum
    invoicecounter_obj.save(update_fields=['invoice_value'])
    return redirect('studentApplicationsview')  

def feepayTerm2(request,student_id):
    obj = academicYear.objects.all()
    obj = list(obj)
    obj = obj[0]
    student_object = studentApplications.objects.get(student_id=student_id)
    fees = enrolledStudents.objects.get(student_enrolled= student_object,academic_year= obj.academic_year)
    fees.Term2flag = 'Y'
    fees.save(update_fields=['Term2flag'])  
    Term2_fee = fees.Term2
    st =  studentInvoice.objects.get(student_id = fees,academic_year=fees.academic_year)
    st.amountpaid = int(st.amountpaid) + int(Term2_fee)
    st.save(update_fields=['amountpaid'])
    return redirect('studentApplicationsview')   

def feepayTerm3(request,student_id):
    obj = academicYear.objects.all()
    obj = list(obj)
    obj = obj[0]
    student_object = studentApplications.objects.get(student_id=student_id)
    fees = enrolledStudents.objects.get(student_enrolled= student_object,academic_year= obj.academic_year)
    fees.Term3flag = 'Y'
    fees.save(update_fields=['Term3flag'])
    Term3_fee = fees.Term3
    st =  studentInvoice.objects.get(student_id = fees,academic_year=fees.academic_year)
    st.amountpaid = int(st.amountpaid) + int(Term3_fee)
    st.save(update_fields=['amountpaid'])  
    return redirect('studentApplicationsview') 

def Removestudent(request,student_id):
    obj = academicYear.objects.all()
    obj = list(obj)
    obj = obj[0]
    student_object = studentApplications.objects.get(student_id=student_id)
    studentremove = enrolledStudents.objects.get(student_enrolled= student_object,academic_year= obj.academic_year)
    studentremove.active_status = 'N'
    student_object.Enrolled = 'N'
    studentremove.save(update_fields=['active_status'])
    student_object.save(update_fields=['Enrolled'])
    return redirect(studentsdata)

def individualstudent(request):
    obj = academicYear.objects.all()
    obj = list(obj)
    obj = obj[0]
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    uid_obj = USER_DETAILS.objects.get(USER_EMAIL=user.email)
    profile = MICRO_APPLY.objects.filter(uid = uid_obj.uid)
    schoolStudent = INDIVIDUAL_WEBPAGESS1.objects.get(uid= uid_obj.uid)
    studentinfo = enrolledStudents.objects.filter(school = schoolStudent,academic_year=obj.academic_year,active_status='Y')
    return render(request,'individualAdminDashboard/individualstudent.html',{'enrolled':studentinfo,'profile':profile})

def IndividualAlumni(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    uid_obj = USER_DETAILS.objects.get(USER_EMAIL=user.email)
    profile = MICRO_APPLY.objects.filter(uid = uid_obj.uid)
    schoolStudent = INDIVIDUAL_WEBPAGESS1.objects.get(uid= uid_obj.uid)
    obj = academicYear.objects.all()
    obj = list(obj)
    obj = obj[0]
    studentinfo = enrolledStudents.objects.filter(school = schoolStudent,active_status='N',academic_year=obj.academic_year)
    return render(request,'individualAdminDashboard/IndividualAlumni.html',{'enrolled':studentinfo,'profile':profile})

'''def enrolledStudents(request,student_id):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    name = user.first_name
    student_obj = studentApplications.objects.get(student_id=student_id)
    student_obj.Enrolled ='Y'
    student_obj.save(update_fields=['Enrolled'])
    print(student_obj.enrolling_grade)
    print(student_obj.enrolling_term)
    feedetails = individual_feedetail.objects.get(admin = student_obj.microschool)
    fees = AffliatesfeeStructure.objects.get(school = feedetails.admin)
    print(fees)
    return redirect('superAdmin_dashboard')'''
    
def notifyUsers(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    uid_obj = USER_DETAILS.objects.get(USER_EMAIL=user.email)
    profile = MICRO_APPLY.objects.filter(uid = uid_obj.uid)
    nu = notify_users.objects.all()
    return render(request,'superAdminDashboard/notifyUsers.html',{'nu':nu,'profile':profile})

def superAdminAlumni(request):
    obj = academicYear.objects.all()
    obj = list(obj)
    obj = obj[0]
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    uid_obj = USER_DETAILS.objects.get(USER_EMAIL=user.email)
    profile = MICRO_APPLY.objects.filter(uid = uid_obj.uid)
    enrolled = enrolledStudents.objects.filter(active_status = 'N',academic_year=obj.academic_year)
    return render(request,'superAdminDashboard/superAdminAlumni.html',{'enrolled':enrolled,'profile':profile})



def studentedit_admin(request,student_id):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    uid_obj = USER_DETAILS.objects.get(USER_EMAIL=user.email)
    profile = MICRO_APPLY.objects.filter(uid = uid_obj.uid)
    student_obj = studentApplications.objects.filter(student_id=student_id)
    student_obj1 = list(student_obj)
    student_obj1 = student_obj1[0]
    DOB = student_obj1. SaaSDOB 
    print(student_obj1. SaaSDOB )
    if request.method == "POST" :
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        #SaaSDOB = request.POST['SaaSDOB']
        enrolling_grade = request.POST['enrolling_grade']
        Fathersname = request.POST['Fathersname']
        Fathersoccupation = request.POST['Fathersoccupation']
        Mothersname = request.POST['Mothersname']
        Mothersoccupation = request.POST['Mothersoccupation']
        address = request.POST['address']
        email = request.POST['email']
        number = request.POST['number']
        geekzcommute = request.POST['geekzcommute']
        yescommutelocation = request.POST['yescommutelocation']
        year = request.POST['year']
        student_edit = studentApplications.objects.get(student_id=student_id)
        student_edit.first_name = first_name
        student_edit.last_name = last_name
        #student_edit.SaaSDOB = SaaSDOB
        student_edit.enrolling_grade = enrolling_grade
        student_edit.Fathersname = Fathersname
        student_edit.Fathersoccupation = Fathersoccupation
        student_edit.Mothersname = Mothersname
        student_edit.address = address
        student_edit.email = email
        student_edit.phone = number
        student_edit. geekzcommute = geekzcommute
        student_edit.yescommutelocation  = yescommutelocation 
        student_edit.enrolling_year = year
        student_edit.save(update_fields=['first_name','last_name','enrolling_grade','Fathersname','Fathersoccupation','Mothersname','address','email','phone','geekzcommute','yescommutelocation','enrolling_year'])
        return redirect('newApplications')
    return render(request,'individualAdminDashboard/studentedit_admin.html',{'student_obj': student_obj,'DOB':DOB,'profile':profile})


def auditionApprove(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    name = user.first_name
    personal_info = MICRO_APPLY.objects.all()
    audition = MICRO_AUDN.objects.filter(IS_COMPLETE='Y',IS_APPROVED='N')
    return render(request,'superAdminDashboard/auditionApprove.html',{'audition':audition,'name':name}) 



def Affliatestracker(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    name = user.first_name
    personal_info = MICRO_APPLY.objects.all()
    audition = MICRO_AUDN.objects.all()
    return render(request,'superAdminDashboard/Affliatestracker.html',{'audition':audition,'personal_info':personal_info,'name':name})

def WebpageTracker(request):
    web = INDIVIDUAL_WEBPAGESS1.objects.all()
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    name = user.first_name
    return render(request,'superAdminDashboard/WebpageTracker.html',{'name':name,'web':web})

def audition_accept(request,uid):
    aud = MICRO_AUDN.objects.filter(uid = uid)
    aud.IS_APPROVED='Y'
    aud.save(update_fields=['IS_APPROVED'])
    mob = MICRO_APPLY.objects.get(uid = uid)
    subject='Audition accepted'
    html_template='socialaccount/email/audition_accept.html'
    html_message=render_to_string(html_template)
    to_email=mob.EMAIL
    message=EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [to_email])
    message.content_subtype='html'
    message.send()
    return redirect('auditionApprove')

def audition_reject(request,uid):
    aud = MICRO_AUDN.objects.filter(uid = uid)
    aud.IS_APPROVED='R'
    mob = MICRO_APPLY.objects.get(uid = uid)
    aud.save(update_fields=['IS_APPROVED'])
    subject='Audition Rejected'
    html_template='socialaccount/email/audition_reject.html'
    html_message=render_to_string(html_template)
    to_email= mob.EMAIL
    message=EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [to_email])
    message.content_subtype='html'
    message.send()
    return redirect('auditionApprove')
   

def Profiling_saas(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    name = user.first_name
    micro = MicroProfile_feedback.objects.filter(Profiling_done='Y')
    return render(request,'superAdminDashboard/Profiling_saas.html',{'micro':micro,'name':name})

def SaaSProfileFeedback(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    name = user.first_name
    micro = MICRO_PROFILING.objects.filter(IS_PROFILINGCOMPLETE='Y',IS_APPROVED='N')
    return render(request,'superAdminDashboard/SaaSProfileFeedback.html',{'micro':micro,'name':name})

def SaaSprofileMessage(request,uid):
    if request.method == "POST" :
        feedback = request.POST['feedback']
        obj_micro = MICRO_PROFILING.objects.get(IS_PROFILINGCOMPLETE='Y',IS_APPROVED='N',uid = uid)
        message = MicroProfile_feedback(uid= uid,Profiling_done='Y',micro=obj_micro,feedback=feedback)
        message.save()
        return redirect('superAdmin_dashboard')
    return render(request,'superAdminDashboard/SaaSprofileMessage.html')



def Profiling_accept(request,uid):
    aud =  MICRO_PROFILING.objects.get(uid = uid)
    aud.IS_APPROVED='Y'
    aud.save(update_fields=['IS_APPROVED'])
    mob = MICRO_APPLY.objects.get(uid = uid)
    subject='Affliation accepted'
    html_template='socialaccount/email/saasprofilingaccept.html'
    html_message=render_to_string(html_template)
    to_email= mob.EMAIL
    message=EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [to_email])
    message.content_subtype='html'
    message.send()
    return redirect('Profiling_saas')

def Profiling_reject(request,uid):
    aud =  MICRO_PROFILING.objects.get(uid = uid)
    aud.IS_APPROVED='R'
    aud.save(update_fields=['IS_APPROVED'])
    mob = MICRO_APPLY.objects.get(uid = uid)
    subject='Affliation Rejected'
    html_template='socialaccount/email/saasprofilingaccept.html'
    html_message=render_to_string(html_template)
    to_email= mob.EMAIL
    message=EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [to_email])
    message.content_subtype='html'
    message.send()
    return redirect('Profiling_saas')    

def webpage_Approve(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    name = user.first_name
    iww = INDIVIDUAL_WEBPAGESS1.objects.filter(IS_COMPLETE='Y',IS_APPROVED='N')
    return render(request,'superAdminDashboard/webpage_Approve.html',{'iww':iww,'name':name})


def viewbanners(request,uid):
    iw = INDIVIDUAL_WEBPAGESS1.objects.filter(uid=uid)
    iw1 = list(iw)
    iw1 = iw1[0]
    gala = Photo_webpage1.objects.filter(gala_admin = iw1)
    return render(request,'superAdminDashboard/viewbanners.html',{'iw':iw,'gala':gala})


def adminprofileEdit(request,uid):
    info = MICRO_APPLY.objects.filter(uid=uid)
    if request.method == "POST" :
        NAME = request.POST['first_name']
        EMAIL= request.POST['EMAIL']
        COUNTRY_CODE = request.POST['COUNTRY_CODE']
        PHONE = request.POST['PHONE']
        info = MICRO_APPLY.objects.get(uid=uid)
        info.NAME=NAME
        info.EMAIL = EMAIL
        info.COUNTRY_CODE = COUNTRY_CODE
        info.PHONE = PHONE
        info.save(update_fields=['NAME','EMAIL','COUNTRY_CODE','PHONE'])
        return redirect('individualAdmin_dashboard')
    return render(request,'individualAdminDashboard/adminprofileEdit.html',{'info':info})

########################## student Dashboard ###########3
def studentDashboard(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    obj = academicYear.objects.all()
    obj = list(obj)
    obj = obj[0]
    info = studentApplications.objects.filter(student_id=user.id,academic_year=obj.academic_year,Profiling_approved='Y')
    studentObj = studentApplications.objects.get(student_id=user.id,academic_year=obj.academic_year,Profiling_approved='Y')
    enrolling_grade = studentObj.enrolling_grade
    ##### Studio
    grade = ''
    name = studentObj.first_name + studentObj.last_name
    if enrolling_grade == 'Pre-K' or enrolling_grade == 'Jr-K' or enrolling_grade == 'Sr-K':
        grade = "Kindergarten studio"
    elif enrolling_grade == '1st Grade' or enrolling_grade =='2nd Grade' or enrolling_grade =='3rd Grade':
        grade = 'Lower Elementary Studio'
    elif enrolling_grade == '4th Grade' or enrolling_grade == '5th Grade' :
        grade = 'Upper Elementary Studio'
    ########
    enrolled = enrolledStudents.objects.filter(active_status = 'Y',academic_year=obj.academic_year,student_enrolled=studentObj)
    enrolled_alumni = enrolledStudents.objects.filter(active_status = 'N',academic_year=obj.academic_year,student_enrolled=studentObj)
    student_active=''
    if enrolled:
        student_active = 'yes'
    else:
        student_active = 'no' 
    if enrolled_alumni:
        student_active = 'left'
                  
    return render(request,'studentDashboard/studentDashboard.html',{'name':name,'enrolled':enrolled,'info':info,'student_active':student_active,'grade':grade,'enrolled_alumni':enrolled_alumni})

def studentfeestatus(request):
    obj = academicYear.objects.all()
    obj = list(obj)
    obj = obj[0]
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    duedates_obj = duedates.objects.all()
    info = studentApplications.objects.filter(student_id=user.id,academic_year=obj.academic_year,Profiling_approved='Y')
    studentObj = studentApplications.objects.get(student_id=user.id,academic_year=obj.academic_year,Profiling_approved='Y')
    enrolling_grade = studentObj.enrolling_grade
    enrolling_term = studentObj. enrolling_term
    feedetails = individual_feedetail.objects.get(admin = studentObj.microschool)
    fees = AffliatesfeeStructure.objects.get(school = feedetails)
    name = studentObj.first_name + studentObj.last_name
    ##### Fee Structure
    grade =''
    Term1 = ''
    Term2 = ''
    Term3 = ''
    Total = ''
    if enrolling_grade == 'Pre-K' or enrolling_grade == 'Jr-K' or enrolling_grade == 'Sr-K':
        grade = "Kindergarten studio"
        if enrolling_term == 'Full Year':
            Term1 = fees.split1_fullYear_kindergarten
            Term2 = fees.split2_fullYear_kindergarten
            Term3 = fees.split3_fullYear_kindergarten
            Total = fees.total_fullYear_kindergarten
        elif enrolling_term == 'Vijayadasami':
            Term1 = fees.split1_fall_kindergarten
            Term2 = fees.split2_fall_kindergarten
            Term3 = "not valid"
            Total = fees.total_fall_kindergarten
        elif enrolling_term == 'Spring':
            Term1 = fees.split1_spring_kindergarten
            Term2 = "not valid"
            Term3 = "not valid"
            Total = fees.total_spring_kindergarten
    elif enrolling_grade == '1st Grade' or enrolling_grade =='2nd Grade' or enrolling_grade =='3rd Grade':
        grade = 'Lower Elementary Studio'
        if enrolling_term == 'Full Year':
            Term1 = fees.split1_fullYear_lowerElementary 
            Term2 = fees.split2_fullYear_lowerElementary 
            Term3 = fees.split3_fullYear_lowerElementary 
            Total = fees.total_fullYear_lowerElementary 
        elif enrolling_term == 'Vijayadasami':
            Term1 = fees.split1_fall_lowerElementary 
            Term2 = fees.split2_fall_lowerElementary 
            Term3 = "not valid"
            Total = fees.total_fall_lowerElementary
        elif enrolling_term == 'Spring':
            Term1 = fees.split1_spring_lowerElementary
            Term2 = "not valid"
            Term3 = "not valid"
            Total = fees.total_spring_lowerElementary
    elif enrolling_grade == '4th Grade' or enrolling_grade == '5th Grade' :
        grade = 'Upper Elementary Studio'
        if enrolling_term == 'Full Year':
            Term1 = fees.split1_fullYear_UpperElementary
            Term2 = fees.split2_fullYear_UpperElementary 
            Term3 = fees.split3_fullYear_UpperElementary
            Total = fees.total_fullYear_UpperElementary
        elif enrolling_term == 'Vijayadasami':
            Term1 = fees.split1_fall_UpperElementary 
            Term2 = fees.split2_fall_UpperElementary 
            Term3 = "not valid"
            Total = fees.total_fall_UpperElementary
        elif enrolling_term == 'Spring':
            Term1 = fees.split1_spring_UpperElementary
            Term2 = "not valid"
            Term3 = "not valid"
            Total = fees.total_spring_UpperElementary
    studentinfo = enrolledStudents.objects.filter(student_enrolled = studentObj, academic_year=obj.academic_year,active_status='Y')
    #invoice = studentInvoice.objects.filter(student_id= studentinfo,academic_year=obj.academic_year)
    student_active=''
    if studentinfo:
        student_active = 'yes'
    else:
        student_active = 'no' 
    return render(request,'studentDashboard/studentfeestatus.html',{'name':name,'info':info,'studentinfo':studentinfo,'student_active': student_active,'duedates':duedates_obj,'Term1':Term1,'Term2':Term2,'Term3':Term3,'Total':Total,'Studio':grade})

def invoice_pdf(request):
    obj = academicYear.objects.all()
    obj = list(obj)
    obj = obj[0]
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    info = studentApplications.objects.filter(student_id=user.id)
    studentObj = studentApplications.objects.get(student_id=user.id)
    name = studentObj.first_name
    studentinfo = enrolledStudents.objects.filter(student_enrolled = studentObj, academic_year=obj.academic_year,active_status='Y')
    return render(request,'studentDashboard/invoice_pdf.html',{'enrolled':studentinfo,'name':name,'info':info})

def studentinvoice_pdf(request,student_id):
    obj = academicYear.objects.all()
    obj = list(obj)
    obj = obj[0]
    studentObj = studentApplications.objects.get(student_id=student_id,academic_year=obj.academic_year,Profiling_approved='Y')
    studentinfo = enrolledStudents.objects.get(student_enrolled = studentObj, academic_year=obj.academic_year,active_status='Y')
    ob = studentInvoice.objects.get(student_id=studentinfo)
    
    data = {
            'geekName': ob.student_id.student_enrolled.first_name+' '+ob.student_id.student_enrolled.last_name, 
            'fathername': ob.student_id.student_enrolled.Fathersname,
            'address': ob.student_id.student_enrolled.address,  
            'num':ob.invoice_no,
            'edTech':ob.edTech,
            'Total':ob.Totalfees,
            'amountpaid':ob.amountpaid,
            'id': ob.student_id.student_enrolled.student_id,
            'date': datetime.date.today(),
    }
    pdf = render_to_pdf('invoice.html',data)
    return HttpResponse(pdf, content_type='application/pdf')


'''
def newenrollmentsStudent(request):
    obj = academicYear.objects.all()
    obj = list(obj)
    obj = obj[0]
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    info = studentApplications.objects.filter(student_id=user.id)
    studentObj = studentApplications.objects.get(student_id=user.id)
    name = studentObj.first_name
    if request.method == "POST" :
        grade =''
        Term1 = ''
        Term2 = ''
        Term3 = ''
        enrolling_grade = request.POST['current_grade']
        enrolling_term = request.POST['current_enrolling_term']
        academic_year = request.POST['academic_year']
        if enrolling_grade == 'Pre-K' or enrolling_grade == 'Jr-K' or enrolling_grade == 'Sr-K':
            grade = "Kindergarten studio"
            if enrolling_term == 'Full Year':
                Term1 = fees.split1_fullYear_kindergarten
                Term2 = fees.split2_fullYear_kindergarten
                Term3 = fees.split3_fullYear_kindergarten
            elif enrolling_term == 'Vijayadasami':
                Term1 = fees.split1_fall_kindergarten
                Term2 = fees.split2_fall_kindergarten
                Term3 = "not valid"
            elif enrolling_term == 'Spring':
                Term1 = fees.split1_spring_kindergarten
                Term2 = "not valid"
                Term3 = "not valid"
        elif enrolling_grade == '1st Grade' or enrolling_grade =='2nd Grade' or enrolling_grade =='3rd Grade':
            grade = 'Lower Elementary Studio'
            if enrolling_term == 'Full Year':
                Term1 = fees.split1_fullYear_lowerElementary 
                Term2 = fees.split2_fullYear_lowerElementary 
                Term3 = fees.split3_fullYear_lowerElementary 
            elif enrolling_term == 'Vijayadasami':
                Term1 = fees.split1_fall_lowerElementary 
                Term2 = fees.split2_fall_lowerElementary 
                Term3 = "not valid"
            elif enrolling_term == 'Spring':
                Term1 = fees.split1_spring_lowerElementary
                Term2 = "not valid"
                Term3 = "not valid"
        elif enrolling_grade == '4th Grade' or enrolling_grade == '5th Grade' :
            grade = 'Upper Elementary Studio'
            if enrolling_term == 'Full Year':
                Term1 = fees.split1_fullYear_UpperElementary
                Term2 = fees.split2_fullYear_UpperElementary 
                Term3 = fees.split3_fullYear_UpperElementary
            elif enrolling_term == 'Vijayadasami':
                Term1 = fees.split1_fall_UpperElementary 
                Term2 = fees.split2_fall_UpperElementary 
                Term3 = "not valid"
            elif enrolling_term == 'Spring':
                Term1 = fees.split1_spring_UpperElementary
                Term2 = "not valid"
                Term3 = "not valid"
        student_tobeEnrolled = studentApplications.objects.filter(student_id=student_id) 
        student_tobeEnrolled = list(student_tobeEnrolled)
        student_tobeEnrolled = student_tobeEnrolled[0]   
        enroll = enrolledStudent(student_enrolled=student_tobeEnrolled,school=student_tobeEnrolled.microschool, active_status='Y',Term1=Term1,Term2=Term2,Term3=Term3,academic_year= academic_year,grade=grade,current_grade=enrolling_grade,current_enrolling_term=enrolling_term)    
        enroll.save()
        return redirect('studentDashboard')
    return render(request,'studentDashboard/newenrollments.html',{'name':name,'academic_year':obj.academic_year,'info':info})
'''
def Transcript_pdf(request):
    obj = academicYear.objects.all()
    obj = list(obj)
    obj = obj[0]
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    info = studentApplications.objects.filter(student_id=user.id)
    studentObj = studentApplications.objects.get(student_id=user.id)
    name = studentObj.first_name
    studentinfo = enrolledStudents.objects.filter(student_enrolled = studentObj, academic_year=obj.academic_year,active_status='N')
    return render(request,'studentDashboard/Transcript_pdf.html',{'name':name,'academic_year':obj.academic_year,'enrolled':studentinfo,'info':info}) 

def studentTranscript_pdf(request,student_id):
    obj = academicYear.objects.all()
    obj = list(obj)
    obj = obj[0]
    ob = studentApplications.objects.get(student_id=student_id)
    studentinfo = enrolledStudents.objects.get(student_enrolled = ob, academic_year=obj.academic_year,active_status='N')
    print(ob.last_name)
    data = {
            'geekName': studentinfo.student_enrolled.first_name + ' ' + studentinfo.student_enrolled.last_name, 
            'fathername': studentinfo.student_enrolled.Fathersname,
            'mothername':studentinfo.student_enrolled.Mothersname,
            'DOB': studentinfo.student_enrolled.SaaSDOB,
            'enrollingGrade':studentinfo.student_enrolled.enrolling_grade,
            'currentgrade':studentinfo.current_grade,
            'address': studentinfo.student_enrolled.address,      
    }
    pdf = render_to_pdf('transcripts.html',data)
    return HttpResponse(pdf, content_type='application/pdf')


def studentprofileEdit(request,student_id):
    obj = academicYear.objects.all()
    obj = list(obj)
    obj = obj[0]
    info = studentApplications.objects.filter(student_id=student_id)
    studentObj = studentApplications.objects.get(student_id=student_id)
    name = studentObj.first_name
    if request.method == "POST" :
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        #SaaSDOB = request.POST['SaaSDOB']
        Fathersname = request.POST['Fathersname']
        Fathersoccupation = request.POST['Fathersoccupation']
        Mothersname = request.POST['Mothersname']
        Mothersoccupation = request.POST['Mothersoccupation']
        address = request.POST['address']
        email = request.POST['email']
        number = request.POST['number']
        geekzcommute = request.POST['geekzcommute']
        yescommutelocation = request.POST['yescommutelocation']
        student_edit = studentApplications.objects.get(student_id=student_id)
        student_edit.first_name = first_name
        student_edit.last_name = last_name
        #student_edit.SaaSDOB = SaaSDOB
        student_edit.Fathersname = Fathersname
        student_edit.Fathersoccupation = Fathersoccupation
        student_edit.Mothersname = Mothersname
        student_edit.address = address
        student_edit.email = email
        student_edit.phone = number
        student_edit. geekzcommute = geekzcommute
        student_edit.yescommutelocation  = yescommutelocation 
        student_edit.save(update_fields=['first_name','last_name','Fathersname','Fathersoccupation','Mothersname','address','email','phone','geekzcommute','yescommutelocation'])
        return redirect('studentDashboard') 
    return render(request,'studentDashboard/studentprofileEdit.html',{'name':name,'info':info})




    




   
    


