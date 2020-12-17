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
import pytz
import httplib2
from googleapiclient.discovery import build  #pip install google-api-python-client
from oauth2client.service_account import ServiceAccountCredentials #pip install oauth2client
from .models import *
#from .forms import SlotCreationForm
from uuid import uuid4
import datetime
from django.http import JsonResponse

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
        return redirect('index')


'''def student_profileEdit(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    print(user)
    user_details=USER_DETAILS.objects.get(USER_EMAIL=user.email)    
    print(user_details) 
    return render(request,"student_profileEdit.html",{"object_details":user_details})  ''' 


####################Django calendar #########################
#Django calendar_admin view to add slots
'''
def CalendarView1(request):
    if request.method == "POST" :
        start_time = request.POST['start_time']
        print(start_time)
        end_time = request.POST['end_time']
        day = request.POST['day']
        time_duration = float(request.POST['duration'])
        start_datetime_object =  datetime.datetime.strptime(start_time, '%H:%M')
        end_datetime_object =  datetime.datetime.strptime(end_time, '%H:%M')
        #start_time = datetime.time(start_time)
        #end_time = datetime.time(end_time)
        def time_slots(start_time, end_time,duration):
            t = start_time
            while t <= end_time:
                yield t.strftime('%H:%M')
                t += datetime.timedelta(minutes=time_duration)
                slot_obj = slots_day1(slot=t.strftime('%H:%M'),day=day,duration=time_duration)
                slot_obj.save()
                print(t.strftime('%H:%M'))
        print(list(time_slots(start_datetime_object, end_datetime_object,time_duration)))
        return render(request,'calendar_admin.html')
    slots_monday = slots_day1.objects.filter(day='Monday')
    slots_tuesday = slots_day1.objects.filter(day='Tuesday') 
    slots_wednesday = slots_day1.objects.filter(day='Wednesday')
    slots_thursday = slots_day1.objects.filter(day='Thursday')
    slots_friday = slots_day1.objects.filter(day='Friday')
    slots_saturday = slots_day1.objects.filter(day='Saturday')
    return render(request,'schedule_admin.html',{'slots_monday':slots_monday,'slots_tuesday':slots_tuesday,'slots_wednesday':slots_wednesday,'slots_thursday':slots_thursday,'slots_friday':slots_friday,'slots_saturday':slots_saturday})         

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

# view for user to pick date and select slot
def calendar_user(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SlotCreationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            schedule_date = form.cleaned_data['schedule_date']
            slot = form.cleaned_data['slot']
            print('sc',type(schedule_date))
            print('slot',slot.id)
            print(type(slot))
            slot_obj = slots_day1.objects.filter(id=slot.id)
            print('slot_obj',slot_obj)
            qq = list(slot_obj)
            print(qq)
            qq = qq[0]
            nn = qq.duration
            start_time = qq.slot
            now = datetime.datetime.now()
            date_obj = now.strftime("%Y-%m-%d")
            start_time = date_obj + " "+ start_time
            start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')
            end_time = start_time + datetime.timedelta(minutes=float(nn))
            print('st',start_time)
            print('et', end_time)
            if schedule_date < datetime.date.today():
                return HttpResponse("Please do not enter past date")    
            else:
                event_obj = EVENTS_SCHEDULE(title="timi",description="audition",start_time=start_time,end_time=end_time,slot=slot,schedule_date=schedule_date)
                event_obj.save()
                return HttpResponse("Success")         
    # if a GET (or any other method) we'll create a blank form
    else:
        form = SlotCreationForm()
        return render(request,"schedule_user.html",{'form': form})

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
        for event in events['items']:
            print (event['start']['dateTime'])
            times.append(event['start']['dateTime'])
        print(times)    
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
        now = datetime.datetime.now()
        date_obj = now.strftime("%Y-%m-%d")
        print(date_obj)
        date_obj = date_obj + " "+ s.slot
        print(date_obj)
        start_time = datetime.datetime.strptime(date_obj, '%Y-%m-%d %H:%M')
        print(start_time.isoformat())
        # filtering slots if the slot is booked
        for gc in times:
            if start_time == gc:
                pass
            else:
                slot_fil.append(s)
    return JsonResponse(slot_fil.values('id','slot'), safe=False) '''




        
    


