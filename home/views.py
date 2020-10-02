from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages

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
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def signup_(request):
    if request.method == "POST":
        first_name=request.POST['firstname']
        last_name=request.POST['lastname']
        email=request.POST['email']
        password=request.POST['password']
        if User.objects.filter(email=email).exists():
            messages.info(request, 'User already registered')
            return render(request, 'login.html')
        else:
            add_user = User.objects.create_user(username=first_name, password=password, email=email, first_name=first_name, last_name=last_name)
            add_user.save()
            messages.info(request, 'Registration Successfull')
            return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')