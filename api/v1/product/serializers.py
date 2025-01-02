from django.contrib.auth.models import User

from rest_framework import serializers

from staff.models import *
from customer.models import Customer
from work_order.models import ModelNumberBasedProducts, WorkOrder, WorkOrderImages, WorkOrderItems
from product.models import Product,MaterialTypeCategory, Materials, MaterialsType, ProductCategory, ProductSubCategory

# write code here
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields=['name','color','item_code','approximate_development_time','product_category','product_sub_category']

class MaterialsSerializer(serializers.ModelSerializer):
    sub_materials = serializers.SerializerMethodField()
    
    class Meta:
        model = Materials
        fields = ['id','name','is_subcategory','image','sub_materials']
    
    def get_sub_materials(self,obj):
        instances = MaterialsType.objects.filter(material=obj,is_deleted=False)
        serialized = SubMaterialsSerializer(instances,many=True).data
        return serialized
    
class SubMaterialsSerializer(serializers.ModelSerializer):
    sub_material_type = serializers.SerializerMethodField()
    
    class Meta:
        model = MaterialsType
        fields = ['id','name','is_subcategory','sub_material_type']
        
    def get_sub_material_type(self,obj):
        instances = MaterialTypeCategory.objects.filter(material_type=obj,is_deleted=False)
        serialized = MaterialTypeCategorySerializer(instances,many=True).data
        return serialized
    
class MaterialTypeCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MaterialTypeCategory
        fields = ['id','name']
        
        
class ProductCategorySerializer(serializers.ModelSerializer):
    sub_categories = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductCategory
        fields = ['id','name','is_subcategory','image','sub_categories']
    
    def get_sub_categories(self,obj):
        instances = ProductSubCategory.objects.filter(product_category=obj,is_deleted=False)
        serialized = ProductSubCategorySerializer(instances,many=True).data
        return serialized
    
class ProductSubCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductSubCategory
        fields = ['id','name']
