from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import UserDetails
#from allauth.account.decorators import verified_email_required
from django.contrib.auth.decorators import login_required

# Create your views here.
#@login_required
def index(request):
    return render(request, 'index.html')


def schoolasaservice(request):
    return render(request, 'schoolasaservice.html')


def homeschool(request):
    return render(request, 'homeschool.html')


def apply(request):
    return render(request, 'apply.html')


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

def logout(request):
    auth.logout(request)
    return redirect('/')

