from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(WorkOrder)
admin.site.register(WorkOrderItems)
admin.site.register(WorkOrderImages)
# admin.site.register(WoodWorkAssign)
admin.site.register(Carpentary)
admin.site.register(Polish)
admin.site.register(Glass)
admin.site.register(Packing)
admin.site.register(ModelNumberBasedProducts)
admin.site.register(WorkOrderStaffAssign)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(ModelNumberBasedProductImages)

@admin.register(WoodWorkAssign)
class WoodWorkAssignAdmin(admin.ModelAdmin):

    # Columns shown in admin list page
    list_display = (
        'date',
        'work_order',
        'material',
        'sub_material',
        'material_type',
        'quantity',
        'rate',
    )

    # Right-side filters
    list_filter = (
        'date',
        'material',
        'material_type',
    )

    # Search box
    search_fields = (
        'work_order__order_no',
        'material__name',
        'quality',
    )

    # Date hierarchy navigation
#     date_hierarchy = 'date'

    # Default ordering
    ordering = ('-date',)

     #  'material_type',
    

    # Readonly fields (if BaseModel has these)
#     readonly_fields = ('created_at', 'updated_at')

    # Group fields in admin form
   