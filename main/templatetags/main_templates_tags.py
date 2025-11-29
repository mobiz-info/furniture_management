import datetime

from decimal import Decimal, ROUND_HALF_UP

from django import template
from django.db.models import Q, Sum
from django.contrib.auth.models import User, Group
from settings.models import PermissionSet
from staff.models import Staff

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
    else:
        employee_details = Staff.objects.get(user=user)
        username = employee_details.get_fullname()  
        user_image = ""
        
    return {
        'username': username,
        'user_image': user_image,
    }

@register.filter
def remove_brackets(value):
     if isinstance(value, str):
        # Convert string representation of list to actual list
        value = eval(value)
        return ', '.join(value)
     


@register.simple_tag(takes_context=True)
def accessible_tabs(context):
    request = context['request']
    user_department = Staff.objects.get(user=request.user)
    permission_set = PermissionSet.objects.filter(department=user_department.department).first()
    if permission_set:
        return ', '.join(permission_set.tabs.split(','))
    return ''


@register.filter
def multiply_round(val1, val2):
    try:
        v1 = Decimal(str(val1))
        v2 = Decimal(str(val2))
        return (v1 * v2).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
    except:
        return "0.00"