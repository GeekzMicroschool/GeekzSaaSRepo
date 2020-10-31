from django.urls import path
from . import views

urlpatterns = [
    path('apply', views.apply, name="apply"),
    path('saasapplication', views.saasapplication, name="saasapplication"),
    path('audition', views.audition, name="audition"),
    path('saasaudition', views.saasaudition, name="saasaudition"),
]