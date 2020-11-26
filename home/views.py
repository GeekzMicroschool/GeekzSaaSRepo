from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from schoolasaservice.models import MICRO_APPLN, QUEST_APPLN, MICRO_AUDN, QUEST_AUDN,MICRO_APPLY
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

'''def searchbar(request):
    if request.method == "POST":
        SaaSLoc_lat=float(request.POST['loc_lat'])
        SaaSLoc_long=float(request.POST['loc_long'])
        user_location = Point( SaaSLoc_long,SaaSLoc_lat)
        for p in MICRO_APPLY.objects.raw('SELECT NAME, SCHOOL_LOCALITY  FROM  MICRO_APPLY  WHERE  location=user_location && ST_Expand(location.geom, 5000)  ORDER BY ST_Distance(location.geom) ASC LIMIT 1;'):
            print(p)
    return render(request,'serachbar.html')  '''     



def search_filter(request):
     return render(request,'search_filter.html')

#@login_required
def index(request):
    return render(request, 'index.html')

def schoolasaservice(request):
    return render(request, 'schoolasaservice.html')

def questschool(request):
    return render(request, 'questschool.html')

def homeschool(request):
    return render(request, 'homeschool.html')

def jobs(request):
    return render(request, 'jobs.html')


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
  

