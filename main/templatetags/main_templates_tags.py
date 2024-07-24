import datetime

from django import template
from django.db.models import Q, Sum
from django.contrib.auth.models import User, Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
        return group in user.groups.all()
    except Group.DoesNotExist:
        return False
    
@register.filter(name='has_department')
def has_department(user, department_name):
    # staff = Staff.objects.get(email=user)
    # print(staff)
    # if staff.department.name.lower() == department_name :
        # return True
    # else:
    return False

@register.simple_tag
def get_username(request):
    user = User.objects.get(username=request.user.username)
    if user.is_superuser==True:
        username = request.user.username
        user_image = ""
    # else:
        # employee_details = Staff.objects.get(user=user)
        username = ""
        user_image = ""
        
    return {
        'username': username,
        'user_image': user_image,
    }