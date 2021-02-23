from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url

#from  Geekz_Microschool import settings
urlpatterns = [
    path('apply', views.apply, name="apply"),
    path('saasapplication', views.saasapplication, name="saasapplication"),
    path('audition', views.audition, name="audition"),
    path('saasaudition', views.saasaudition, name="saasaudition"),
    path("student_profileEdit",views.student_profileEdit,name="sp"),
    path('schedule_admin', views.schedule_admin, name="schedule_admin"),
    path('profiling', views.profiling, name="profiling"),
    path('saasappointment',views.saasappointment,name="saasappointment"),
    path('ajax/load_slots/', views.load_slots, name='ajax_load_slots'), # AJAX
    path('web_form',views.web_form,name='web_form'),
    path('rough',views.rough,name="rough"),
    path('webpage_creation',views.webpage_creation,name='webpage_creation'),
    path('webpage',views.webpage,name='webpage'),
    path('microschool/<LOCALITY>',views.webpage, name='webpage'),
    path('deletevent',views.deletevent,name="delete"),
    path('superAdmin_dashboard',views.superAdmin_dashboard,name="delete"),
    path('bs-basic-table',views.basictables,name="delete"),
    path('invoice',views.GeneratePdf,name="generatepdf"),
    path('create_pdf',views.create_pdf,name="create_pdf"),
    path('index1',views.index1,name="index1"),
    path('geekzmicro',views.school_template,name="geekzmicro"),
    path('web1',views.web1,name="web1"),
    path('rough2',views.rough2,name="rough2"),
    path('bulk_load',views.bulk_load,name="bulk_load"),
    #path('drag_load',views.drag_load,name="drag_load"),
    path('clear',views.clear_database,name="clear"),
    path('affliateslist',views.affliateslist,name="affliateslist"),
    path('affliates_List',views.affliates_List,name="affliates_List"),
    path('notify',views.notify,name="notify"),
    path('affliatesform',views.affliates_form,name="affliatesform"),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
