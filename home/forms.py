from allauth.account.forms import SignupForm
from django import forms
from .models import UserDetails

from django.core.validators import FileExtensionValidator


class SimpleSignupForm(SignupForm):
    email = forms.EmailField(max_length=255)
    fullname = forms.CharField(max_length=200)
    phone_no = forms.IntegerField()
    sameasphone = forms.BooleanField(required=False)
    whatsapp_no = forms.IntegerField(required=False)

    def save(self, request):
    	# first call save of parent class
        user = super(SimpleSignupForm, self).save(request)
        
        if self.cleaned_data['sameasphone'] == True:
            whatsapp_no = self.cleaned_data['phone_no']
        else:
            try:
                whatsapp_no = self.cleaned_data['whatsapp_no']
            except:
                whatsapp_no = ''

        # Now create new models
        UserDetails.objects.create(email = user.email, fullname = self.cleaned_data['fullname'], phone_no = self.cleaned_data['phone_no'], whatsapp_no = whatsapp_no)
        return user