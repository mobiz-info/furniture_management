import datetime

from django import template
from django.db.models import Q, Sum

from work_order.forms import WorkOrderStatusForm
from work_order.models import *

register = template.Library()

@register.simple_tag
def work_order_status_assign_form():
    return WorkOrderStatusForm()

@register.simple_tag
def get_work_order_costs(work_order):
    wood_cost = WoodWorkAssign.objects.filter(work_order=work_order).aggregate(total=Sum('rate'))['total'] or 0
    labour_cost = WorkOrderStaffAssign.objects.filter(work_order=work_order).aggregate(total=Sum('wage'))['total'] or 0

    accessories_carpentary = Carpentary.objects.filter(work_order=work_order).aggregate(total=Sum('rate'))['total'] or 0
    accessories_polish = Polish.objects.filter(work_order=work_order).aggregate(total=Sum('rate'))['total'] or 0
    accessories_glass = Glass.objects.filter(work_order=work_order).aggregate(total=Sum('rate'))['total'] or 0
    accessories_packing = Packing.objects.filter(work_order=work_order).aggregate(total=Sum('rate'))['total'] or 0

    accessories_total = (
        wood_cost +
        accessories_carpentary +
        accessories_polish +
        accessories_glass +
        accessories_packing
    )
        
    total_cost = wood_cost + labour_cost + accessories_total


    return {
        'labour_cost': labour_cost,
        'accessories_total': accessories_total,
        'total_cost': total_cost,
    }
