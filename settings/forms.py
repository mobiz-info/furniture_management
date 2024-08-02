from datetime import date

from django import forms
from django.forms import formset_factory, inlineformset_factory
from django.forms.widgets import TextInput,Textarea,Select,DateInput,CheckboxInput,FileInput,PasswordInput
from django.forms import TextInput, URLInput, EmailInput

from . models import *


class CompanyDetailsForm(forms.ModelForm):
    
    class Meta:
        model = CompanyDetails
        fields = ['name','address','gst','concerned_staff','designation','mobile','email','username','password','mode']

        widgets = {
            'name': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter company name'}), 
            'address': TextInput(attrs={'type':'text','class': ' required form-control', 'placeholder' : 'Enter address'}),
            'gst': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter gst'}),
            'concerned_staff': TextInput(attrs={'type':'text','class': ' required form-control', 'placeholder' : 'Enter concerned staff'}),
            'designation': Select(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter designation'}), 
            'mobile': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter mobile'}), 
            'email': EmailInput(attrs={'type':'text','class': ' required form-control', 'placeholder' : 'Enter email'}),
            'username': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter username'}),
            'password': PasswordInput(attrs={'type':'text','class': ' required form-control', 'placeholder' : 'Enter password'}),
            'mode': Select(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter mode'}), 
            
        }
class CompanyDetailsEditForm(forms.ModelForm):
    
    class Meta:
        model = CompanyDetails
        fields = ['name','address','gst','concerned_staff','designation','mobile','email','username','mode']

        widgets = {
            'name': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter company name'}), 
            'address': TextInput(attrs={'type':'text','class': ' required form-control', 'placeholder' : 'Enter address'}),
            'gst': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter gst'}),
            'concerned_staff': TextInput(attrs={'type':'text','class': ' required form-control', 'placeholder' : 'Enter concerned staff'}),
            'designation': Select(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter designation'}), 
            'mobile': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter mobile'}), 
            'email': EmailInput(attrs={'type':'text','class': ' required form-control', 'placeholder' : 'Enter email'}),
            'username': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter username'}),
            'mode': Select(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter mode'}), 
            
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

class BranchForm(forms.ModelForm):
    
    class Meta:
        model = Branch
        fields = ['name','location','latitude','longitude','image']

        widgets = {
            'name': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter Branch Name'}), 
            'location': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter Location'}),
            'latitude': TextInput(attrs={'type':'text','class': ' required form-control', 'placeholder' : 'Enter Latitude'}),
            'longitude': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter Longitude'}), 
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }

