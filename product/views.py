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
from product.forms import MaterialTypeCategoryForm, MaterialsForm, MaterialsTypeForm
from product.models import Materials, MaterialsType
from rest_framework import status
#local
from main.decorators import role_required
from main.functions import generate_form_errors, get_auto_id, has_group

# Create your views here.
@login_required
@role_required(['superadmin'])
def material_info(request,pk):
    """
    Material List
    :param request:
    :return: Material List single view
    """
    
    instances = Materials.objects.get(pk=pk)

    context = {
        'instances': instances,
        'page_name' : 'Material Info',
        'page_title' : 'Material Info',
    }

    return render(request, 'admin_panel/pages/product/materials/info.html', context)

@login_required
@role_required(['superadmin'])
def material_list(request):
    """
    material
    :param request:
    :return: material list view
    """
    filter_data = {}
    query = request.GET.get("q")
    
    instances = Materials.objects.filter(is_deleted=False).order_by("-date_added")
    
    if query:
        instances = instances.filter(
            Q(invoice_no__icontains=query) |
            Q(sales_id__icontains=query) 
        )
        title = "material list - %s" % query
        filter_data['q'] = query
    
    context = {
        'instances': instances,
        'page_name' : 'Materials List',
        'page_title' : 'Materials List',
        'filter_data' :filter_data,
    }

    return render(request, 'admin_panel/pages/product/materials/list.html', context)

@login_required
@role_required(['superadmin'])
def create_material(request):
    MaterialsTypeFormset = formset_factory(MaterialsTypeForm, extra=2)
    
    message = ''
    if request.method == 'POST':
        material_form = MaterialsForm(request.POST)
        material_type_formset = MaterialsTypeFormset(request.POST,prefix='material_type_formset', form_kwargs={'empty_permitted': False})
        
        form_is_valid = False
        if material_form.is_valid():
            form_is_valid = True
            if material_form.cleaned_data.get("is_subcategory"):
                if not material_type_formset.is_valid():
                    form_is_valid = False
        
        if  form_is_valid :
            
            material_data = material_form.save(commit=False)
            material_data.auto_id = get_auto_id(Materials)
            material_data.creator = request.user
            material_data.save()
            
            for form in material_type_formset:
                material_type = form.save(commit=False)
                material_type.auto_id = get_auto_id(MaterialsType)
                material_type.creator = request.user
                material_type.material = material_data
                material_type.save()
                
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Materials created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('product:material_list')
            }
    
        else:
            message = generate_form_errors(material_form, formset=False)
            if material_form.cleaned_data.get("is_subcategory"):
                message += generate_form_errors(material_type_formset, formset=True)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
    else:
        material_form = MaterialsForm(request.POST)
        material_type_formset = MaterialsTypeFormset(prefix='material_type_formset')
        
        context = {
            'material_form': material_form,
            'material_type_formset': material_type_formset,
            
            'page_name' : 'Create Material',
            'page_title': 'Create Materials',
            'url': reverse('product:create_material'),
            
            'material_page': True,
            'is_need_select2': True,
            
        }
        
        return render(request,'admin_panel/pages/product/materials/create.html',context)
    
    
@login_required
@role_required(['superadmin'])
def edit_material(request,pk):
    """
    edit operation of material
    :param request:
    :param pk:
    :return:
    """
    material_instance = get_object_or_404(Materials, pk=pk)
    metirial_types = MaterialsType.objects.filter(material=material_instance)
    
    if MaterialsType.objects.filter(material=material_instance).exists():
        m_extra = 0
    else:
        m_extra = 1 
        
    MeterialsFormset = inlineformset_factory(
        Materials,
        MaterialsType,
        extra=m_extra,
        form=MaterialsTypeForm,
    )
    
    message = ''
    
    if request.method == 'POST':
        material_type_formset = MeterialsFormset(request.POST,request.FILES,
                                        instance=material_instance,
                                        prefix='material_type_formset',
                                        form_kwargs={'empty_permitted': False})    
                
        if material_type_formset.is_valid() :
            #create
            for form in material_type_formset:
                if form not in material_type_formset.deleted_forms:
                    i_data = form.save(commit=False)
                    if not i_data.material :
                        i_data.material = material_instance
                    i_data.save()
                
                
            for f in material_type_formset.deleted_forms:
                f.instance.delete()
            
            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Materials Updated Successfully.",
                'redirect': 'true',
                "redirect_url": reverse('product:material_list'),
            }
    
        else:
            message = generate_form_errors(material_type_formset,formset=True)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
                        
    else:
        material_type_formset = MeterialsFormset(queryset=metirial_types,
                                        prefix='material_type_formset',
                                        instance=material_instance)
        
        context = {
            'material_type_formset': material_type_formset,
            'message': message,
            'page_name' : 'Edit Material',
            'url' : reverse('material:edit_sales', args=[material_instance.pk]),            
        }

        return render(request, 'admin_panel/pages/material/create_sale.html', context)