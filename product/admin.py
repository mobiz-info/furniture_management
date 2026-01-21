from django.contrib import admin

from . models import MaterialTypeCategory, Materials, MaterialsType, Product,ProductCategory,ProductSubCategory

# Register your models here.
# class MaterialsAdmin(admin.ModelAdmin):
#     list_display = [
#         'id','name','is_subcategory'
#     ]
# admin.site.register(Materials,MaterialsAdmin)

@admin.register(Materials)
class MaterialsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_subcategory',
        'amount',
        
    )
    # Filters on right side
    list_filter = (
        'is_subcategory',
    )
    # Search bar
    search_fields = (
        'name',
    )

    # Default ordering
    ordering = ('name',)

class MaterialsTypeAdmin(admin.ModelAdmin):
    list_display = [
        'id','name','material','is_subcategory'
    ]
admin.site.register(MaterialsType,MaterialsTypeAdmin)


class MaterialTypeCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id','name','material_type'
    ]
admin.site.register(MaterialTypeCategory,MaterialTypeCategoryAdmin)

# class MaterialTypeCategoryAdmin(admin.ModelAdmin):
#     list_display = [
#         'id','name','material_type'
#     ]
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductSubCategory)
