#standerd
import json
import random
import datetime
from datetime import date, timedelta
#django
from django.urls import reverse
from django.conf import settings
from django.db.models import Sum
from django.utils import timezone
from django.http import JsonResponse
from django.utils.html import strip_tags
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,Group
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse
# third party
from rest_framework import status
#local
from main.decorators import role_required
from . forms import ForgotPasswordForm, PasswordGenerationForm
from main.functions import decrypt_message, encrypt_message, generate_form_errors, generate_member_form_errors, has_group

@login_required
def app(request):
  
    return HttpResponseRedirect(reverse('main:index'))

# Create your views here.
@login_required
# @role_required(['superadmin'])
def index(request):
    today_date = timezone.now().date()
    last_month_start = (today_date - timedelta(days=today_date.day)).replace(day=1)
    
    context = {
        'page_name' : 'Dashboard',
    }
  
    return render(request,'admin_panel/index.html', context)


# def forgot_password(request):
    
#     if request.method == 'POST':
#         form = ForgotPasswordForm(request.POST)

#         if form.is_valid():
#             username = form.cleaned_data['username']
#             if not '@' in username:
#                 username = username.upper()
#                 if (instances:=CoreTeam.objects.filter(employee_id=username)).exists():
#                     instance = instances.first()
#                 elif (instances:=OfficeExecutive.objects.filter(employee_id=username)).exists():
#                     instance = instances.first()
#             else:
#                 if (instances:=CoreTeam.objects.filter(email=username)).exists():
#                     instance = instances.first()
#                 elif (instances:=OfficeExecutive.objects.filter(email=username)).exists():
#                     instance = instances.first()
                
#             encrypt_id = encrypt_message(instance.employee_id)
#             base_url = request.scheme + "://" + request.get_host()
#             mail_html = render_to_string('registration/change_password_mail.html', {'user_data': instance, 'encrypt_id':encrypt_id,'base_url':base_url})
#             if settings.SERVER :
#                 mail_message = strip_tags(mail_html)
#                 send_email("FMS Change Password",instance.email,mail_message,mail_html)
#             else:
#                 print(mail_html)           
                
#             response_data = {
#                 "status": "true",
#                 "title": "Successful",
#                 "message": "Check your registered email address for a password reset link. It should arrive in your inbox shortly.",
#                 'redirect': 'true',
#                 'redirect_url': reverse("main:mail_success")
#             }
#             status_code = status.HTTP_200_OK
#         else:
#             # print("not valid")
#             message = generate_form_errors(form, formset=False)
#             # print(message)
#             status_code = status.HTTP_400_BAD_REQUEST
#             response_data = {
#                 "status": "false",
#                 "message": message,
#             }
            
#         return HttpResponse(json.dumps(response_data),status=status_code, content_type="application/json")
        
#     else :
#         form = ForgotPasswordForm()

#         context = {
#             'form': form,
#         }
    
#         return render(request,'registration/forgot_password.html', context)
        

def mail_success(request):
    return render(request,'registration/email-success.html')


def change_password(request,employee_id):
    
    if request.method == 'POST':
        form = PasswordGenerationForm(request.POST)

        if form.is_valid():
            username = decrypt_message(employee_id).upper()
             
            # usr = User.objects.get(username=instance.email)
            # usr.set_password(form.cleaned_data['password'])
            # usr.save()
            
            # update employee password
            # instance.date_updated = datetime.datetime.today()
            # instance.updater = usr
            # instance.password = encrypt_message(form.cleaned_data['password'])
            # instance.save()
            
            response_data = {
                "status": "true",
                "title": "Successful",
                "message": "Password Updated Successfully",
                'redirect': 'true',
                'redirect_url': reverse("main:change_password_success")
            }
            status_code = status.HTTP_200_OK
        else:
            message = generate_form_errors(form, formset=False)
            status_code = status.HTTP_400_BAD_REQUEST
            response_data = {
                "status": "false",
                "message": message,
            }
            
        return HttpResponse(json.dumps(response_data),status=status_code, content_type="application/json")
        
    else :
        form = PasswordGenerationForm()

        context = {
            'form': form,
        }
    
        return render(request,'registration/change_password.html', context)