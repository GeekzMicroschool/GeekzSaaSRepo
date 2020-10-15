from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('schoolasaservice', views.schoolasaservice, name="schoolasaservice"),
    path('homeschool', views.homeschool, name="homeschool"),
    path('apply', views.apply, name="apply"),
    path('jobs', views.jobs, name="jobs"),
    path('logout', views.logout, name="logout"),
    #path('gsignup', views.gsignup, name="gsignup"),
    #path('glogin', views.glogin, name="glogin"),
    #path('login', views.login, name="login"),
    #path('signup', views.signup, name="signup"),
]