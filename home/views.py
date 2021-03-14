from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from schoolasaservice.models import MICRO_APPLN, QUEST_APPLN, MICRO_AUDN, QUEST_AUDN,MICRO_APPLY
from schoolasaservice.models import *
from .models import USER_DETAILS
#from allauth.account.decorators import verified_email_required
from django.contrib.auth.decorators import login_required
from django.contrib.gis.db.models.functions import Distance
from allauth.account.signals import user_logged_in, user_signed_up
from django.dispatch import receiver
from django.views import generic
#for sending email
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.gis.measure import Distance
from django.contrib.gis.geos import Point
from django.db.models.query import QuerySet

#from allauth.socialaccount.models import SocialAccount

'''from django.dispatch import receiver
from allauth.socialaccount.signals import pre_social_login'''


# Create your views here.

# search feature for user
def searchbar(request):
    if request.method == "POST":
        SaaSLoc_lat=float(request.POST['loc_lat'])
        SaaSLoc_long=float(request.POST['loc_long'])
        user_location = Point( SaaSLoc_long,SaaSLoc_lat)
        cr = MICRO_APPLY.objects.values()
        clients = cr.filter(location__distance_lt=(user_location,Distance(m=5000)))
        print(type(clients))
       # clients = clients_within_radius.filter(location=(user_location,Distance(m=5000)))
       # print(type(clients))
        #course_qs = <whatever query gave you the queryset>
        for course in clients:
            print(course['NAME'])
        #print(clients[0])
        return render(request,'search_filter.html',{'clients_within_radius':clients})    
    return render(request,'serachbar.html')



def search_filter(request):
     return render(request,'search_filter.html')

#### landing page #######
#@login_required
def index(request):
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
    return render(request,'index.html')        
    

def locationnotvalid(request):
    return render(request,'locationnotvalid.html')

def notify(request):
    if request.method == "POST" :
        email = request.POST['email']
        phone = request.POST['phone']
        not_obj = notify_users(email = email ,phone= phone )
        not_obj.save()
        return render(request,'affliatesnotfound.html')

def searchresults(request):
    if request.method == "POST" :
        SaaSLoc_lat=request.POST['loc_lat']
        SaaSLoc_long=request.POST['loc_long']
        def is_float1(SaaSLoc_lat):
            try:
                num = float(SaaSLoc_lat)
            except ValueError:
                return False
            return True

        def is_float2(SaaSLoc_long):
            try:
                num = float(SaaSLoc_long)
            except ValueError:
                return False
            return True

        if is_float1(SaaSLoc_lat) and is_float2(SaaSLoc_long):
            SaaSLoc_lat = float(SaaSLoc_lat)
            SaaSLoc_long = float(SaaSLoc_long)

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
        else:
            return redirect('locationnotvalid')


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


#@login_required
'''def index(request):
    return render(request, 'index.html')'''

def schoolasaservice(request):
    return render(request, 'schoolasaservice.html')

def questschool(request):
    return render(request, 'questschool.html')

def homeschool(request):
    return render(request, 'homeschool.html')

def jobs(request):
    return render(request, 'jobs.html')

@login_required
def Account_Email(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    print(user.email)
    if USER_DETAILS.objects.filter(USER_EMAIL=user.email):
        session = USER_DETAILS.objects.get(USER_EMAIL=user.email)
        if MICRO_PROFILING.objects.filter(uid= session.uid):
            return redirect('individualAdmin_dashboard')
        else:
            return redirect('index')    
    elif studentApplications.objects.filter(student_id=user.id):
        if studentApplications.objects.filter(student_id=user.id,Profiling_approved='Y'):
            return redirect('studentDashboard')
        else:
            return redirect('index') 
    elif user.email == 'admin@g.com':
        return redirect('superAdmin_dashboard')
    else:
        return redirect('index') 



               
    

#@verified_email_required
'''
def login(request):
    if request.method == "POST":
        email=request.POST['email']
        password=request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None and user.is_superuser == False:
            print("usseer",user)
            auth.login(request, user)
            return render(request, 'index.html')
        else:
            print("usseer",user)
            return render(request, 'index.html')


def signup(request):
    if request.method == "POST":
        fullname=request.POST['fullname']
        email=request.POST['email']
        password=request.POST['password']
        phone_no=request.POST['phoneno']
        try:
            sameasphone=request.POST['sameasphone']
            if sameasphone == 'yes':
                whatsapp_no=phone_no
            else:
                whatsapp_no=request.POST['whatsappno']
        except:
            whatsapp_no=request.POST['whatsappno']
        if User.objects.filter(email=email).exists():
            messages.info(request, 'User already registered')
            return render(request, 'index.html')
        else:
            add_user = User.objects.create_user(email=email, password=password, username=email)
            add_user.save()
            add_user_details = UserDetails(email=email, fullname=fullname, phone_no=phone_no, whatsapp_no=whatsapp_no)
            add_user_details.save()
            messages.info(request, 'Registration Successfull')
            return render(request, 'index.html')

'''
'''
def glogin(request):
    def populate_user(self, request, sociallogin, data):
        print("sdsdsd",sociallogin.account.user)
        return render(request, 'index.html')
    populate_user()
    return render(request, 'index.html')'''

'''
def gsignup(request):
    print("In google signup")
    print("user",user)
    print("user id",user.id)
    return render(request, 'index.html')'''

def logout(request):
    auth.logout(request)
    return redirect('/')


@receiver(user_signed_up)
def sendwelcomemail(request, user, **kwargs):
    #welcome mail
    subject='Welcome to Geekz!'
    html_template='socialaccount/email/welcome_email.html'
    html_message=render_to_string(html_template)
    to_email=user.email
    message=EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [to_email])
    message.content_subtype='html'
    message.send()


'''
@receiver(user_signed_up)
def retrieve_social_data(request, user, **kwargs):
    print("in signal user signed up")
    print("userrrrrrr",user)
    print("userid",user.id)
    user_tb_detail=User.objects.get(id=user.id)
    social_data=SocialAccount.objects.get(user_id=user.id)
    user_tb_detail.id=social_data.uid
    user_tb_detail.save()
    print("daaata",data)
    print("data picture",data[0].get_avatar_url())
    """Signal, that gets extra data from sociallogin and put it to profile."""
    # get the profile where i want to store the extra_data
    #profile = Profile(user=user)
    # in this signal I can retrieve the obj from SocialAccount
    data = SocialAccount.objects.filter(user=user, provider='facebook')
    # check if the user has signed up via social media
    if data:
        picture = data[0].get_avatar_url()
        if picture:
            # custom def to save the pic in the profile
            save_image_from_url(model=profile, url=picture)
        profile.save()'''

#for getting session
@receiver(user_logged_in)
def post_login(request, user, **kwargs):
    request.session['user_id']=user.id

@login_required
def student_profileEdit(request):
    user_id=request.session['user_id']
    user=User.objects.get(id=user_id)
    print(user)
    user_details=USER_DETAILS.objects.get(USER_EMAIL=user.email)    
    return render(request,"student_profileEdit.html",{"user_details":user_details})      
  

