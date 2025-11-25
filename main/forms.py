from django import forms
from django.contrib.auth.models import User,Group

from rest_framework import status


class PasswordGenerationForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'})
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Re-enter Password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        if password and len(password) < 8:
            raise forms.ValidationError("Please enter a minimum of 8 characters")

        if password and len(password) > 20:
            raise forms.ValidationError("Please enter a maximum of 20 characters for the password")

        return cleaned_data
    
    

class ForgotPasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter email id or employee id'}))
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        
        if not '@' in username:
            username = username.upper()
            # if (instances:=Staff.objects.filter(employee_id=username)).exists():
            #     instances.first().email
            # else:
            #     raise forms.ValidationError("Employee ID not found please contact admin")
        
        # elif User.objects.filter(username=username).exists() and not Staff.objects.filter(email=username).exists():
        #     pass
        # else:
        #   raise forms.ValidationError("username not found please contact admin")
      
        return cleaned_data