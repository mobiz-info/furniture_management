import datetime
from decimal import Decimal, ROUND_HALF_UP

from django import template
from django.db.models import Q, Sum
from django.db.models import F, FloatField, Sum, ExpressionWrapper

from work_order.forms import WorkOrderStatusForm
from work_order.models import *

register = template.Library()


def to_decimal(val):
    return Decimal(str(val)).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)

@register.simple_tag
def work_order_status_assign_form():
    return WorkOrderStatusForm()

@register.simple_tag
def get_work_order_costs(work_order):
    # Labour cost
    labour_cost = WorkOrderStaffAssign.objects.filter(work_order=work_order).aggregate(
        total=Sum('wage')
    )['total'] or 0

    # Helper to calculate rate * quantity
    def calculate_total_cost(model):
        return model.objects.filter(work_order=work_order).annotate(
            qty_float=ExpressionWrapper(F('quantity'), output_field=FloatField()),
            total_cost=ExpressionWrapper(F('rate') * F('qty_float'), output_field=FloatField())
        ).aggregate(total=Sum('total_cost'))['total'] or 0

    # Calculate accessories cost using rate * quantity
    wood_cost = calculate_total_cost(WoodWorkAssign)
    carpentary_cost = calculate_total_cost(Carpentary)
    polish_cost = calculate_total_cost(Polish)
    glass_cost = calculate_total_cost(Glass)
    packing_cost = calculate_total_cost(Packing)

    accessories_total = wood_cost + carpentary_cost + polish_cost + glass_cost + packing_cost
    total_cost = float(labour_cost) + float(accessories_total)

    return {
        'labour_cost': round(labour_cost, 2),
        'accessories_total': round(accessories_total, 2),
        'total_cost': round(total_cost, 2),
    }
    
@register.simple_tag
def get_accessories_by_work_order(work_order):
    from decimal import Decimal, ROUND_HALF_UP

    def to_decimal(val):
        return Decimal(str(val)).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)

    def get_data(section_name, queryset):
        data = []
        for item in queryset:

            # convert to decimal safely
            try:
                quantity = to_decimal(item.quantity)
            except:
                quantity = Decimal("0.00")

            rate = to_decimal(item.rate)
            total_cost = to_decimal(quantity * rate)

            data.append({
                'date_added': item.date_added,
                'section': section_name,
                'material': item.material.name,
                'sub_material': item.sub_material.name,
                'material_type': item.material_type.name,
                'rate': rate,               # --> always two decimals
                'quantity': quantity,       # --> always two decimals
                'total_cost': total_cost,   # --> always two decimals
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
        'total_rate': total_rate.quantize(Decimal("0.00")),
        'total_quantity': total_quantity.quantize(Decimal("0.00")),
        'total_cost': total_cost.quantize(Decimal("0.00")),
    }
