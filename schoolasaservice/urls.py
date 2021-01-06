from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
#from  Geekz_Microschool import settings
urlpatterns = [
    path('apply', views.apply, name="apply"),
    path('saasapplication', views.saasapplication, name="saasapplication"),
    path('audition', views.audition, name="audition"),
    path('saasaudition', views.saasaudition, name="saasaudition"),
    path("student_profileEdit",views.student_profileEdit,name="sp"),
    path('schedule_admin', views.schedule_admin, name="schedule_admin"),
    path('schedule_user', views.schedule_user, name="schedule_user"),
    path('ajax/load_slots/', views.load_slots, name='ajax_load_slots'), # AJAX
    path('web_form',views.web_form,name='web_form'),
    path('webpage_creation',views.webpage_creation,name='webpage_creation'),
    path('webpage',views.webpage,name='webpage'),
    path('microschool/<url>',views.webpage, name='webpage'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
