from datetime import date

from django import forms
from django.forms import formset_factory, inlineformset_factory
from django.forms.widgets import TextInput,Textarea,Select,DateInput,CheckboxInput,FileInput,PasswordInput
from django.forms import TextInput, URLInput, EmailInput

from . models import *


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']

        widgets = {
            'name': TextInput(attrs={
                'type': 'text',
                'class': 'required form-control',
                'placeholder': 'Enter Department Name'
            }),
        }

class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ['name', 'department']

        widgets = {
            'name': TextInput(attrs={
                'type': 'text',
                'class': 'required form-control',
                'placeholder': 'Enter Designation Name'
            }),
            'department': forms.Select(attrs={
                'class': 'required form-control'
            }),
        }
        
class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        
        fields = ['first_name', 'last_name', 'designation', 'department', 'phone', 'address', 'email', 'employee_id']
        
        widgets = {
            'first_name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Enter Last Name'}),
            'designation': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Address'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'employee_id': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Enter Employee ID'}),
        }
        
        

class AttendenceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['date', 'punchin_time', 'punchout_time', 'attendance']
        
        widgets = {
            'date' : forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Enter Date', 'readonly': True}),
            'punchin_time' : forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'placeholder': 'Select Time'}),
            'punchout_time' : forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'placeholder': 'Select Time'}),
            'attendance' : forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Attendece Type'}),
        }
    
