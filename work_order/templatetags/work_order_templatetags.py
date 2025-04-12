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
    
@register.simple_tag
def get_accessories_by_work_order(work_order):
    def get_data(section_name, queryset):
        data = []
        for item in queryset:
            try:
                quantity = float(item.quantity)
            except:
                quantity = 0.0
            rate = float(item.rate)
            total_cost = quantity * rate
            data.append({
                'date_added': item.date_added,
                'section': section_name,
                'material': item.material.name,
                'rate': rate,
                'quantity': quantity,
                'total_cost': total_cost,
            })
        return data

    accessories = []
    accessories += get_data('Wood Work', WoodWorkAssign.objects.filter(work_order=work_order, is_deleted=False))
    accessories += get_data('Carpentary', Carpentary.objects.filter(work_order=work_order, is_deleted=False))
    accessories += get_data('Polish', Polish.objects.filter(work_order=work_order, is_deleted=False))
    accessories += get_data('Glass', Glass.objects.filter(work_order=work_order, is_deleted=False))
    accessories += get_data('Packing', Packing.objects.filter(work_order=work_order, is_deleted=False))

    total_rate = sum(item['rate'] for item in accessories)
    total_quantity = sum(item['quantity'] for item in accessories)
    total_cost = sum(item['total_cost'] for item in accessories)

    return {
        'items': accessories,
        'total_rate': total_rate,
        'total_quantity': total_quantity,
        'total_cost': total_cost,
    }
