from django.shortcuts import render

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