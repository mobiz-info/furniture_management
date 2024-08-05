from django.contrib import admin

from . models import MaterialTypeCategory, Materials, MaterialsType, Product,ProductCategory

# Register your models here.
class MaterialsAdmin(admin.ModelAdmin):
    list_display = [
        'id','name','is_subcategory'
    ]
admin.site.register(Materials,MaterialsAdmin)


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
