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
from settings.forms import *
from settings.models import *
from rest_framework import status

#local
from main.decorators import role_required
from main.functions import generate_form_errors, get_auto_id, has_group

@login_required
@role_required(['superadmin'])
def company_details_info(request,pk):
    """
    company details List
    :param request:
    :return: company details List single view
    """
    
    instances = CompanyDetails.objects.get(pk=pk)

    context = {
        'instances': instances,
        'page_name' : 'Company Details',
        'page_title' : 'Company Details',
    }

    return render(request, 'settings/company_details_info.html', context)

@login_required
@role_required(['superadmin'])
def company_details_list(request):
    """
    company_details
    :param request:
    :return: company_details list view
    """
    filter_data = {}
    query = request.GET.get("q")
    
    instances = CompanyDetails.objects.filter(is_deleted=False).order_by("-date_added")
    
    if query:
        instances = instances.filter(
            Q(name__icontains=query) |
            Q(location__icontains=query) 
        )
        title = "comapny details list - %s" % query
        filter_data['q'] = query
    
    context = {
        'instances': instances,
        'page_name' : 'Company Details List',
        'page_title' : 'Company Details List',
        'filter_data' :filter_data,
    }

    return render(request, 'settings/company_details_list.html', context)

@login_required
@role_required(['superadmin'])
def company_details_create(request):
    """
    create operation of company details
    :param request:
    :param pk:
    :return:
    """
    if request.method == 'POST':
        form = CompanyDetailsForm(request.POST)
        
        form_is_valid = False
        if form.is_valid():
            form_is_valid = True
           
        if  form_is_valid :
            
            data = form.save(commit=False)
            data.auto_id = get_auto_id(CompanyDetails)
            data.creator = request.user
            data.save()
            
            
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Company Details created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('settings:company_details_list')
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
        form = CompanyDetailsForm(request.POST)
        
        context = {
            'form': form,
            'page_name' : 'Create Material',
            'page_title': 'Create Materials',
            'url': reverse('settings:company_details_create'),
            
            'material_page': True,
            'is_need_select2': True,
            
        }
        
        return render(request,'settings/company_details_create.html',context)
    
@login_required
@role_required(['superadmin'])
def company_details_edit(request,pk):
    """
    edit operation of company_details
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(CompanyDetails, pk=pk)
        
    message = ''
    if request.method == 'POST':
        form = CompanyDetailsForm(request.POST,files=request.FILES,instance=instance)
        
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
                    
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Company Details Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('settings:company_details_list')
            }
    
        else:
            message = generate_form_errors(form ,formset=False)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
    else:
        
        form = CompanyDetailsForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Edit Sales Party',
            'page_title' : 'Edit Sales Party',
            'url' : reverse('settings:company_details_edit', kwargs={'pk': pk}),
            
            'is_need_datetime_picker': True,
            'is_need_forms': True,
        }

        return render(request, 'settings/company_details_edit.html',context)    
    
@login_required
@role_required(['superadmin'])
def company_details_delete(request, pk):
    """
    SalesParty deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    instance = CompanyDetails.objects.get(pk=pk)
    
    instance.is_deleted = True
    instance.save()
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Sales Party Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('settings:company_details_list'),
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

#--------------------------------Contact-----------------------------------------
@login_required
@role_required(['superadmin'])
def contact_info(request, pk):
    """
    Contact List
    :param request:
    :return: Contact List single view
    """
    
    instances = get_object_or_404(Contact, pk=pk)
    context = {
        'instances': instances,
        'page_name': 'Contact Info',
        'page_title': 'Contact Info',
    }
    return render(request, 'admin_panel/pages/contact/info.html', context)

@login_required
@role_required(['superadmin'])

def contact_list(request):
    """
    contact
    :param request:
    :return: contact list view
    """

    instances = Contact.objects.filter(is_deleted=False).order_by("-date_added")
    context = {
        'instances': instances,
        'page_name': 'Contact List',
        'page_title': 'Contact List',
    }
    return render(request, 'admin_panel/pages/contact/list.html', context)


@login_required
@role_required(['superadmin'])
def create_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.creator = request.user
            contact.auto_id = get_auto_id(Contact)
            contact.save()
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Contact created successfully.",
                "redirect": "true",
                "redirect_url": reverse('settings:contact_list')
            }
            return HttpResponse(json.dumps(response_data), content_type='application/javascript')
        else:
            message = generate_form_errors(form, formset=False)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }
            return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = ContactForm()
        context = {
            'form': form,
            'page_name': 'Create Contact',
            'page_title': 'Create Contact',
            'url': reverse('settings:create_contact')
        }
        return render(request, 'admin_panel/pages/contact/create.html', context)

@login_required
@role_required(['superadmin'])
def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Contact updated successfully.",
                "redirect": "true",
                "redirect_url": reverse('settings:contact_list')
            }
            return HttpResponse(json.dumps(response_data), content_type='application/javascript')
        else:
            message = generate_form_errors(form, formset=False)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }
            return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = ContactForm(instance=contact)
        context = {
            'form': form,
            'page_name': 'Edit Contact',
            'page_title': 'Edit Contact',
            'url': reverse('settings:edit_contact', args=[contact.pk])
        }
        return render(request, 'admin_panel/pages/contact/edit.html', context)

@login_required
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.is_deleted = True
    contact.save()
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Contact deleted successfully.",
        "redirect": "true",
        "redirect_url": reverse('settings:contact_list')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

# Branch
@login_required
@role_required(['superadmin'])
def branch_info(request,pk):
    """
    branch List
    :param request:
    :return: company details List single view
    """
    
    instances = Branch.objects.get(pk=pk)

    context = {
        'instances': instances,
        'page_name' : 'Branch',
        'page_title' : 'Branch',
    }

    return render(request, 'settings/branch_info.html', context)

@login_required
@role_required(['superadmin'])
def branch_list(request):
    """
    branch_details
    :param request:
    :return: company_details list view
    """
    filter_data = {}
    query = request.GET.get("q")
    
    instances = Branch.objects.filter(is_deleted=False).order_by("-date_added")
    
    if query:
        instances = instances.filter(
            Q(name__icontains=query) |
            Q(location__icontains=query) 
        )
        title = "branch details list - %s" % query
        filter_data['q'] = query
    
    context = {
        'instances': instances,
        'page_name' : 'Branch Details List',
        'page_title' : 'Branch Details List',
        'filter_data' :filter_data,
    }

    return render(request, 'settings/branch_list.html', context)

@login_required
@role_required(['superadmin'])
def branch_create(request):
    """
    create operation of company details
    :param request:
    :param pk:
    :return:
    """
    if request.method == 'POST':
        form = BranchForm(request.POST)
        
        form_is_valid = False
        if form.is_valid():
            form_is_valid = True
           
        if  form_is_valid :
            
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Branch)
            data.creator = request.user
            data.save()
            
            
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Branch created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('settings:branch_list')
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
        form = BranchForm(request.POST)
        
        context = {
            'form': form,
            'page_name' : 'Create Branch',
            'page_title': 'Create Branch',
            'url': reverse('settings:branch_create'),
            
            'material_page': True,
            'is_need_select2': True,
            
        }
        
        return render(request,'settings/branch_create.html',context)
    
@login_required
@role_required(['superadmin'])
def branch_edit(request,pk):
    """
    edit operation of branch_details
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Branch, pk=pk)
        
    message = ''
    if request.method == 'POST':
        form = BranchForm(request.POST,files=request.FILES,instance=instance)
        
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
                    
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Branch Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('settings:branch_list')
            }
    
        else:
            message = generate_form_errors(form ,formset=False)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
    else:
        
        form = BranchForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Edit Branch',
            'page_title' : 'Edit Branch',
            'url' : reverse('settings:branch_edit', kwargs={'pk': pk}),
            
            'is_need_datetime_picker': True,
            'is_need_forms': True,
        }

        return render(request, 'settings/branch_edit.html',context)    
    
@login_required
@role_required(['superadmin'])
def branch_delete(request, pk):
    """
    branch deletion
    :param request:
    :param pk:
    :return:
    """
    instance = Branch.objects.get(pk=pk)
    
    instance.is_deleted = True
    instance.save()
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Branch Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('settings:branch_list'),
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')