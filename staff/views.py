from django.shortcuts import render
import io
import json
import random
import datetime
from datetime import timezone
#django
from django.db.models import Q,Sum,Min,Max 
from django.forms import formset_factory, inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import transaction
# rest framework
from staff.forms import *
from staff.models import *
from rest_framework import status

#local
from main.decorators import role_required
from main.functions import generate_form_errors, get_auto_id, has_group
# Create your views here.
#department
@login_required
@role_required(['superadmin'])
def department_info(request, pk):
    """
    Department List
    :param request:
    :return: Department details List single view
    """
    
    instance = get_object_or_404(Department, pk=pk)

    context = {
        'instances': instance,
        'page_name': 'Department',
        'page_title': 'Department',
    }

    return render(request,'admin_panel/pages/department/department_info.html', context)

@login_required
@role_required(['superadmin'])
def department_list(request):
    """
    Department details
    :param request:
    :return: Department details list view
    """
    filter_data = {}
    query = request.GET.get("q")
    
    instances = Department.objects.filter(is_deleted=False).order_by("-date_added")
    
    if query:
        instances = instances.filter(
            Q(name__icontains=query)
        )
        title = "Department details list - %s" % query
        filter_data['q'] = query
    
    context = {
        'instances': instances,
        'page_name': 'Department Details List',
        'page_title': 'Department Details List',
        'filter_data': filter_data,
    }

    return render(request,'admin_panel/pages/department/department_list.html', context)

@login_required
@role_required(['superadmin'])
def department_create(request):
    """
    Create operation of department details
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        
        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Department)
            data.creator = request.user
            data.save()
            
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Department created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('staff:department_list')
            }
    
        else:
            message = generate_form_errors(form, formset=False)
           
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
    else:
        form = DepartmentForm()
        
        context = {
            'form': form,
            'page_name': 'Create Department',
            'page_title': 'Create Department',
            'url': reverse('staff:department_create'),
        }
        
        return render(request,'admin_panel/pages/department/department_create.html', context)
    
@login_required
@role_required(['superadmin'])
def department_edit(request, pk):
    """
    Edit operation of department details
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Department, pk=pk)
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=instance)
        
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
                    
            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Department updated successfully.",
                'redirect': 'true',
                "redirect_url": reverse('staff:department_list')
            }
    
        else:
            message = generate_form_errors(form, formset=False)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
    else:
        form = DepartmentForm(instance=instance)

        context = {
            'form': form,
            'page_name': 'Edit Department',
            'page_title': 'Edit Department',
            'url': reverse('staff:department_edit', kwargs={'pk': pk}),
        }

        return render(request,'admin_panel/pages/department/department_edit.html', context)
    

@login_required
@role_required(['superadmin'])
def department_delete(request, pk):
    """
    Department deletion
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Department, pk=pk)
    
    instance.is_deleted = True
    instance.save()
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Department successfully deleted.",
        "redirect": "true",
        "redirect_url": reverse('staff:department_list'),
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin'])
def designation_info(request, pk):
    """
    Designation List
    :param request:
    :return: Designation details List single view
    """
    
    instance = get_object_or_404(Designation, pk=pk)

    context = {
        'instances': instance,
        'page_name': 'Designation',
        'page_title': 'Designation',
    }

    return render(request,'admin_panel/pages/designation/designation_info.html', context)

@login_required
@role_required(['superadmin'])
def designation_list(request):
    """
    Designation details
    :param request:
    :return: Designation details list view
    """
    filter_data = {}
    query = request.GET.get("q")
    
    instances = Designation.objects.filter(is_deleted=False).order_by("-date_added")
    
    if query:
        instances = instances.filter(
            Q(name__icontains=query)
        )
        title = "Designation details list - %s" % query
        filter_data['q'] = query
    
    context = {
        'instances': instances,
        'page_name': 'Designation Details List',
        'page_title': 'Designation Details List',
        'url': reverse('staff:designation_list'),
        'filter_data': filter_data,
    }

    return render(request, 'admin_panel/pages/designation/designation_list.html', context)

@login_required
@role_required(['superadmin'])
def designation_create(request):
    """
    Create operation of designation details
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = DesignationForm(request.POST)
        
        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Designation)
            data.creator = request.user
            data.save()
            
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Designation created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('staff:designation_list')
            }
    
        else:
            message = generate_form_errors(form, formset=False)
           
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
    else:
        form = DesignationForm()
        
        context = {
            'form': form,
            'page_name': 'Create Designation',
            'page_title': 'Create Designation',
            'url': reverse('staff:designation_create'),
        }
        
        return render(request, 'admin_panel/pages/designation/designation_create.html', context)

@login_required
@role_required(['superadmin'])
def designation_edit(request, pk):
    """
    Edit operation of designation details
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Designation, pk=pk)
    
    if request.method == 'POST':
        form = DesignationForm(request.POST, instance=instance)
        
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
                    
            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Designation updated successfully.",
                'redirect': 'true',
                "redirect_url": reverse('staff:designation_list')
            }
    
        else:
            message = generate_form_errors(form, formset=False)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
    else:
        form = DesignationForm(instance=instance)

        context = {
            'form': form,
            'page_name': 'Edit Designation',
            'page_title': 'Edit Designation',
            'url': reverse('staff:designation_edit', kwargs={'pk': pk}),
        }

        return render(request,'admin_panel/pages/designation/designation_edit.html', context)

@login_required
@role_required(['superadmin'])
def designation_delete(request, pk):
    """
    Designation deletion
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Designation, pk=pk)
    
    instance.is_deleted = True
    instance.save()
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Designation successfully deleted.",
        "redirect": "true",
        "redirect_url": reverse('staff:designation_list'),
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')