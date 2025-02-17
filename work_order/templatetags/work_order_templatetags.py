import datetime

from django import template
from django.db.models import Q, Sum

from work_order.forms import WorkOrderStatusForm

register = template.Library()

@register.simple_tag
def work_order_status_assign_form():
    return WorkOrderStatusForm()

   