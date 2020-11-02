from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *

# Register your models here.
admin.site.register(MICRO_APPLN)
admin.site.register(QUEST_APPLN)
admin.site.register(MICRO_AUDN)
admin.site.register(QUEST_AUDN)
