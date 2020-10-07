from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import UserDetails

# Create your views here.
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


def login(request):
    if request.method == "POST":
        email=request.POST['email']
        password=request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None and user.is_superuser == False:
            auth.login(request, user)
            return render(request, 'index.html')
        else:
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


def logout(request):
    auth.logout(request)
    return redirect('/')

