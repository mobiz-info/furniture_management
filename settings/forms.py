from datetime import date

from django import forms
from django.forms import formset_factory, inlineformset_factory
from django.forms.widgets import TextInput,Textarea,Select,DateInput,CheckboxInput,FileInput,PasswordInput

from . models import *


class CompanyDetailsForm(forms.ModelForm):
    
    class Meta:
        model = CompanyDetails
        fields = ['name','address','location','latitude','longitude','image']

        widgets = {
            'name': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter Company Name'}), 
            'address': TextInput(attrs={'type':'text','class': ' required form-control', 'placeholder' : 'Enter Address'}),
            'location': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter Location'}),
            'latitude': TextInput(attrs={'type':'text','class': ' required form-control', 'placeholder' : 'Enter Latitude'}),
            'longitude': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter Longitude'}), 
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }
        

        

