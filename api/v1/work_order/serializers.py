from django.contrib.auth.models import User,Group

from main.functions import get_auto_id
from rest_framework import serializers
from work_order.models import *

class WorkOrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    status_value = serializers.SerializerMethodField()
    
    class Meta:
        model = WorkOrder
        fields=['order_no','customer','status','delivery_date','total_estimate','status_value','customer_name']
        
    def get_status_value(self,obj):
        return obj.get_status_display()
    
    def get_customer_name(self,obj):
        return obj.customer.name

class WoodWorkAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model=WoodWorkAssign
        fields=['work_order','material','sub_material','material_type','quality','quantity','rate']

class CarpentarySerializer(serializers.ModelSerializer):
    class Meta:
        model=Carpentary
        fields=['work_order','material','sub_material','material_type','quality','quantity','rate']

class PolishSerializer(serializers.ModelSerializer):
    class Meta:
        model=Polish
        fields=['work_order','material','sub_material','material_type','quality','quantity','rate']

class GlassSerializer(serializers.ModelSerializer):
    class Meta:
        model=Glass
        fields=['work_order','material','sub_material','material_type','quality','quantity','rate']

class PackingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Packing
        fields=['work_order','material','sub_material','material_type','quality','quantity','rate']
        

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'mobile_number', 'address', 'email', 'gst_no']
        

class WorkOrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderItems
        fields = [
            'category', 'sub_category', 'model_no', 'material', 
            'sub_material', 'material_type', 'quantity', 'remark', 
            'estimate_rate', 'size', 'color'
        ]


class WorkOrderImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderImages
        fields = ['image', 'remark']


class CreateWorkOrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    work_order_items = WorkOrderItemsSerializer(many=True, read_only=True)
    work_order_images = WorkOrderImagesSerializer(many=True, read_only=True)

    class Meta:
        model = WorkOrder
        fields = [
            'customer', 'order_no', 'remark', 'total_estimate', 
            'delivery_date', 'work_order_items', 'work_order_images'
        ]

class ModelNumberBasedProductsSerializer(serializers.ModelSerializer):
    category_id = serializers.CharField(source='category.pk', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    sub_category_id = serializers.CharField(source='sub_category.pk', read_only=True)
    sub_category_name = serializers.CharField(source='sub_category.name', read_only=True)
    material_id = serializers.CharField(source='material.pk', read_only=True)
    material_name = serializers.CharField(source='material.name', read_only=True)
    material_type_id = serializers.CharField(source='material_type.pk', read_only=True)
    material_type_name = serializers.CharField(source='material_type.name', read_only=True)
    
    class Meta:
        model = ModelNumberBasedProducts
        fields = ['model_no','category_id','sub_category_id','material_id','sub_material_id','material_type_id','color','category_name','sub_category_name','material_name','sub_material_name','material_type_name']
        
        
class ModelOrderNumbersSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ModelNumberBasedProducts
        fields = ['model_no']