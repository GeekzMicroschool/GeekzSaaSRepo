from django.urls import path
from . import views

urlpatterns = [
    path('apply', views.apply, name="apply"),
    path('saasapplication', views.saasapplication, name="saasapplication"),
    path('audition', views.audition, name="audition"),
    path('saasaudition', views.saasaudition, name="saasaudition"),
    #path("student_profileEdit",views.student_profileEdit,name="sp")
    path('schedule_admin', views.schedule_admin, name="schedule_admin"),
    path('schedule_user', views.schedule_user, name="schedule_user"),
    path('ajax/load_slots/', views.load_slots, name='ajax_load_slots'), # AJAX
    
]