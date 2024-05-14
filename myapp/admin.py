from django.contrib import admin

from .models import Diseases , Doctors, DoctorInfo

admin.site.register(Diseases)
admin.site.register(Doctors)
admin.site.register(DoctorInfo)
