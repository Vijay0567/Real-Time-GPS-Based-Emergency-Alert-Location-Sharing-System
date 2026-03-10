from django.contrib import admin
from .models import Profile, EmergencyContact, AccidentReport


admin.site.register(Profile)
admin.site.register(EmergencyContact)
admin.site.register(AccidentReport)