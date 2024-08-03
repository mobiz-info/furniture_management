from django.shortcuts import render, redirect,get_object_or_404
from .forms import WoodWorkOrderForm
from .models import *
import datetime
from datetime import timezone

from django.http import JsonResponse
from django.db import transaction, IntegrityError
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import WoodWorkOrderForm
from .models import WoodWorkOrder
from main.functions import generate_form_errors, get_auto_id
#local
from settings.forms import *
from settings.models import *
from main.decorators import role_required
from django.http import HttpResponse
import json

from .forms import *

@login_required
@role_required(['superadmin'])
def workorder(request):
    if request.method == 'POST':
        form = WoodWorkOrderForm(request.POST, request.FILES)
        customer_form = CustomerForm(request.POST, request.FILES)
        images_formset = WoodWorkOrderImagesFormSet(request.POST, request.FILES, prefix='images')
        assign_formset = WoodWorkAssignFormSet(request.POST, prefix='assignments')

        if form.is_valid() and customer_form.is_valid() and images_formset.is_valid() and assign_formset.is_valid():
            try:
                with transaction.atomic():
                    # Save the Customer instance
                    customer = customer_form.save(commit=False)
                    customer.user = request.user 
                    customer.auto_id = get_auto_id(Customer)  # Assign auto_id
                    customer.creator = request.user
                    customer.save()

                    # Save the WorkOrder instance
                    work_order = form.save(commit=False)
                    work_order.customer = customer
                    work_order.auto_id = get_auto_id(WoodWorkOrder)  # Assign auto_id
                    work_order.creator = request.user
                    work_order.save()

                    # Save the images formset
                    for image_form in images_formset:
                        if image_form.is_valid():
                            image_instance = image_form.save(commit=False)
                            image_instance.work_order = work_order
                            image_instance.auto_id = get_auto_id(WoodWorkOrderImages)  # Assign auto_id
                            image_instance.creator = request.user
                            image_instance.save()

                    # Handle WoodWorkAssign formset
                    for assign_form in assign_formset:
                        if assign_form.is_valid():
                            assign_instance = assign_form.save(commit=False)
                            assign_instance.work_order = work_order
                            assign_instance.auto_id = get_auto_id(WoodWorkAssign)  # Assign auto_id
                            assign_instance.creator = request.user
                            assign_instance.save()

                    response_data = {
                        "status": "true",
                        "title": "Successfully Created",
                        "message": "Work Order created successfully.",
                        'redirect': 'true',
                        "redirect_url": reverse('work_order:work_order_list')
                    }
                    return JsonResponse(response_data)

            except Exception as e:
                response_data = {
                    "status": "false",
                    "title": "Failed",
                    "message": str(e),
                }
                return JsonResponse(response_data)

    else:
        form = WoodWorkOrderForm()
        customer_form = CustomerForm()
        images_formset = WoodWorkOrderImagesFormSet(prefix='images')
        assign_formset = WoodWorkAssignFormSet(prefix='assignments')

    context = {
        'form': form,
        'customer_form': customer_form,
        'images_formset': images_formset,
        'assign_formset': assign_formset
    }

    return render(request, 'admin_panel/pages/order/workorder.html', context)



@login_required
@role_required(['superadmin'])

def work_order_list(request):
    """
    :param request:
    :return: work order list view
    """

    instances = WoodWorkOrder.objects.filter(is_deleted=False).order_by("-date_added")
    context = {
        'instances': instances,
        'page_name': 'Work Order List',
        'page_title': 'Work Order List',
    }
    return render(request, 'admin_panel/pages/order/work_order_list.html', context)

