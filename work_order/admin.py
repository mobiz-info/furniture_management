from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(WorkOrder)
admin.site.register(WorkOrderItems)
admin.site.register(WorkOrderImages)
admin.site.register(WoodWorkAssign)