from datetime import date

from django import forms
from django.forms import formset_factory, inlineformset_factory
from django.forms.widgets import TextInput,Textarea,Select,DateInput,CheckboxInput,FileInput,PasswordInput
from django.forms import TextInput, URLInput, EmailInput

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
        

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['phone', 'instagram_url', 'facebook_url', 'gmail']

        widgets = {
            'phone': TextInput(attrs={'type':'text','class': 'required form-control','placeholder': 'Enter Phone Number'}),
            'instagram_url': URLInput(attrs={'class': 'required form-control','placeholder': 'Enter Instagram URL'}),
            'facebook_url': URLInput(attrs={'class': 'form-control','placeholder': 'Enter Facebook URL'}),
            'gmail': EmailInput(attrs={'class': 'required form-control','placeholder': 'Enter Gmail Address'}),
        }

