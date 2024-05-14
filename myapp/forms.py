from django import forms
from .models import Doctors

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctors
        fields = ['name', 'specialization', 'qualification', 'experience', 'contact_number', 'email', 'password']
