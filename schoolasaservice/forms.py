from django.forms import ModelForm, DateInput
from schoolasaservice.models import SLOTS_DAY,MICRO_PROFILIN,Photo_webpage1,StudentProfiling,Individual_admin_slots
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
import calendar
import datetime
slot_obj = []

class SlotCreationForm(forms.ModelForm):
  '''schedule_date = forms.DateField(widget= forms.DateInput(attrs={
    "type":"date",
    "placeholder":"%Y-%m-%d",
    "class":"form-control"
  }))'''
  
  class Meta:
    model = MICRO_PROFILIN
    fields = ['schedule_date','slot']
    max =  datetime.date.today() + datetime.timedelta(days=14)
    print(max)
    min = datetime.date.today() + datetime.timedelta(days=1)
    widgets = {
      'schedule_date': DateInput(attrs={'class':'form-control','onfocus':"(this.type='date')",'placeholder':'Schedule Date','min':min ,'max': max }, format='%Y-%m-%d'),
      } 
   
  
  def __init__(self, *args, **kwargs):
    super(SlotCreationForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['schedule_date'].input_formats = ('%Y-%m-%d',)
    self.fields['slot'].queryset = SLOTS_DAY.objects.none()
    if 'schedule_date' in self.data:
            try:
              schedule_date = self.data.get('schedule_date')
              print(schedule_date)
              def findDay(date):
                born = datetime.datetime.strptime(date, '%Y-%m-%d').weekday() 
                return (calendar.day_name[born]) 
              self.fields['slot'].queryset = SLOTS_DAY.objects.filter(day=findDay(schedule_date)).all()
            except (ValueError, TypeError):
              pass  # invalid input from the client; ignore and fallback to empty City queryset
    #elif self.instance.pk:
     #       self.fields['city'].queryset = self.instance.country.city_set.order_by('name')

 # def __init__(self, *args, **kwargs):
  #   super().__init__(*args, **kwargs)
   #  self.fields['slot'].queryset = slots_day1.objects.none()'''

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo_webpage1
        fields = ('file', )

   
          
class IndividualSlotCreationForm(forms.ModelForm):
  '''schedule_date = forms.DateField(widget= forms.DateInput(attrs={
    "type":"date",
    "placeholder":"%Y-%m-%d",
    "class":"form-control"
  }))'''
  
  class Meta:
    model = StudentProfiling
    fields = ['schedule_date','slot']
    max =  datetime.date.today() + datetime.timedelta(days=14)
    print(max)
    min = datetime.date.today() + datetime.timedelta(days=1)
    widgets = {
      'schedule_date': DateInput(attrs={'class':'form-control','onfocus':"(this.type='date')",'placeholder':'Schedule Date','min':min ,'max': max }, format='%Y-%m-%d'),
      } 
   
  
  def __init__(self, *args, **kwargs):
    super(IndividualSlotCreationForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['schedule_date'].input_formats = ('%Y-%m-%d',)
    self.fields['slot'].queryset = Individual_admin_slots.objects.none()
    if 'schedule_date' in self.data:
            try:
              schedule_date = self.data.get('schedule_date')
              print(schedule_date)
              def findDay(date):
                born = datetime.datetime.strptime(date, '%Y-%m-%d').weekday() 
                return (calendar.day_name[born]) 
              self.fields['slot'].queryset = Individual_admin_slots.objects.filter(day=findDay(schedule_date)).all()
            except (ValueError, TypeError):
              pass  # invalid input from the client; ignore and fallback to empty City queryset
    #elif self.instance.pk:
     #       self.fields['city'].queryset = self.instance.country.city_set.order_by('name')

 # def __init__(self, *args, **kwargs):
  #   super().__init__(*args, **kwargs)
   #  self.fields['slot'].queryset = slots_day1.objects.none()'''          