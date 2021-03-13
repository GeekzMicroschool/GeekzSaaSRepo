from django.urls import path
from . import views
from schoolasaservice.views import *


urlpatterns = [
    path('', views.index, name="index"),
    path('index', views.index, name="index"),
    path('schoolasaservice', views.schoolasaservice, name="schoolasaservice"),
    path('questschool', views.questschool, name="questschool"),
    path('homeschool', views.homeschool, name="homeschool"),
    path('jobs', views.jobs, name="jobs"),
    path('logout', views.logout, name="logout"),
    #path('gsignup', views.gsignup, name="gsignup"),
    #path('glogin', views.glogin, name="glogin"),
    #path('login', views.login, name="login"),
    #path('signup', views.signup, name="signup"),
    path('serachbar',views.searchbar,name="searchbar"),
    path('search_filter',views.search_filter,name="search_filter"),
    path('student_profileEdit',views.student_profileEdit,name="spe"),
    path('microschool/<LOCALITY>',views.webpage, name='webpage'),
]  
    