from django.shortcuts import render, redirect
from .models import MICRO_APPLN, QUEST_APPLN, MICRO_AUDN, QUEST_AUDN
from home.models import USER_DETAILS
from django.contrib.auth.models import User,auth
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
#for sending email
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

# Create your views here.
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
        SaaSSchoolCity=request.POST['SaaSSchoolCity']
        SaaSBusiness=request.POST['SaaSBusiness']
        SaaSLinkedin=request.POST['SaaSLinkedin']
        SaaSOccupation=request.POST['SaaSOccupation']
        SaaSPassion=request.POST['SaaSPassion']
        SaaSWhyAffiliate=request.POST['SaaSWhyAffiliate']

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
                new_mschool=MICRO_APPLN(
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

                new_mschool=MICRO_APPLN(
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
                new_mschool=MICRO_APPLN(
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

                new_mschool=MICRO_APPLN(
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
    user_details=USER_DETAILS.objects.get(USER_EMAIL=user.email)
    if user_details.IS_MICROSCHOOL=="Y" or user_details.IS_QUESTSCHOOL=="Y":
        #only show audition form if one of the application is submitted
        if user_details.IS_MICROSCHOOL=="Y":
            #ask for financial field in form because it is microschool
            return render(request, 'audition.html',{'financial':'yes'})
        elif user_details.IS_MICROSCHOOL=="Y" and user_details.IS_QUESTSCHOOL=="Y":
            #ask for financial field in form because it is both microschool and questschool
            return render(request, 'audition.html',{'financial':'yes'})
        else:
            #it is a questschool so don't ask for financial field
            return render(request, 'audition.html')
    else:
        #show application form
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

        if user_details.IS_MICROSCHOOL=="Y":
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
        elif user_details.IS_QUESTSCHOOL=="Y":
            #store in QUEST_AUDN table only
            new_qaudition=MICRO_AUDN(
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

            new_qaudition=MICRO_AUDN(
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
        return render(request, 'auditiondone.html')
