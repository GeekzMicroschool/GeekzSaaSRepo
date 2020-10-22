from allauth.account.forms import SignupForm
from django import forms
from .models import UserDetails

from django.core.validators import FileExtensionValidator

from allauth.socialaccount.forms import SignupForm as SocialSignupForm

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from django.forms.widgets import Input
    
class TelInput(Input):
    input_type = 'tel'

class SimpleSignupForm(SignupForm):
    email = forms.EmailField(max_length=255, widget=forms.EmailInput(attrs={'class':'input-field', 'placeholder':'Email'}))
    fullname = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'input-field', 'placeholder':'Full Name'}))
    phone_no = forms.CharField(widget=TelInput(attrs={'placeholder':'Phone...', 'autocomplete':'off', 'maxlength':'10', 'pattern':'[0-9]{10}'}))
    sameasphone = forms.BooleanField(label=("Get Important Notifications On WhatsApp"), required=False, initial=True)

    def save(self, request):
    	# first call save of parent class
        user = super(SimpleSignupForm, self).save(request)
        country_code = request.POST['countrycode']
        phoneno=self.cleaned_data['phone_no']
        phone_no="+"+country_code+phoneno
        if self.cleaned_data['sameasphone'] == True:
            whatsapp_no = phone_no
        else:
           whatsapp_no = ''

        # Now create new models
        UserDetails.objects.create(email = user.email, fullname = self.cleaned_data['fullname'], phone_no = phone_no, whatsapp_no = whatsapp_no)
        return user


class CustomSocialSignupForm(SocialSignupForm):
    phone_no = forms.CharField(widget=TelInput(attrs={'placeholder':'Phone...', 'autocomplete':'off', 'maxlength':'10', 'pattern':'[0-9]{10}'}))
    sameasphone = forms.BooleanField(label=("Get Important Notifications On WhatsApp"), required=False, initial=True)

    def save(self, request):
        user = super(CustomSocialSignupForm, self).save(request)

        if self.cleaned_data['sameasphone'] == True:
            whatsapp_no = self.cleaned_data['phone_no']
        else:
            whatsapp_no = ''
        fullname = user.first_name+" "+user.last_name
        UserDetails.objects.create(email = user.email, fullname = fullname, phone_no = self.cleaned_data['phone_no'], whatsapp_no = whatsapp_no)

        #welcome mail
        subject='Welcome to Geekz!'
        html_template='socialaccount/email/welcome_email.html'
        html_message=render_to_string(html_template,{'user':user.first_name})
        to_email=user.email
        message=EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [to_email])
        message.content_subtype='html'
        message.send()
        return user