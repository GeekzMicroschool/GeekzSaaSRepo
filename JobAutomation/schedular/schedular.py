import logging
from django.core.mail import EmailMessage
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from django_apscheduler.jobstores import register_events, register_job
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import render, redirect
from schoolasaservice.models import MICRO_APPLN, QUEST_APPLN, MICRO_AUDN, QUEST_AUDN,MICRO_APPLY
from home.models import USER_DETAILS
from django.contrib.auth.models import User,auth
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required



# Create scheduler to run in a thread inside the application process
scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)
def auditionemailjob(request):
    subject='Complete Geekz SaaS Affiliate Profiling!'
    html_template='socialaccount/email/application_received_email.html'
    html_message=render_to_string(html_template)
    to_email='chauhanreetika45@gmail.com'
    message=EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [to_email])
    message.content_subtype='html'
    message.send()


def start():
    if settings.DEBUG:
      	# Hook into the apscheduler logger
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    # Adding this job here instead of to crons.
    # This will do the following:
    # - Add a scheduled job to the job store on application initialization
    # - The job will execute a model class method at midnight each day
    # - replace_existing in combination with the unique ID prevents duplicate copies of the job

    scheduler.add_job(auditionemailjob, 'interval', seconds=30, name='clean_accounts', jobstore='default')
    # Add the scheduled jobs to the Django admin interface
    register_events(scheduler)

    scheduler.start()