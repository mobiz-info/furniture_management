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