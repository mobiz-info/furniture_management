from django.contrib.auth.models import User,Group

from main.functions import get_auto_id
from rest_framework import serializers
from work_order.models import *

class WorkOrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    status_value = serializers.SerializerMethodField()
    
    class Meta:
        model = WorkOrder
        fields=['id','order_no','customer','status','delivery_date','total_estimate','status_value','customer_name']
        read_only_fields=['id']
        
    def get_status_value(self,obj):
        return obj.get_status_display()
    
    def get_customer_name(self,obj):
        return obj.customer.name

class WorkOrderAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model=WorkOrderStatus
        fields=['to_section','description']

class WoodWorkAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model=WoodWorkAssign
        fields=['work_order','material','sub_material','material_type','quality','quantity','rate']
        extra_kwargs = {
            'work_order': {'required': False} 
        }

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
        
class WorkOrderImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderImages
        fields = ['id','work_order','image', 'remark']
        read_only_fields=['id','work_order']
    



class WorkOrderItemsSerializer(serializers.ModelSerializer):
  #  work_order_images = WorkOrderImagesSerializer(many=True, read_only=True)
    class Meta:
        model = WorkOrderItems
        fields = [
            'category', 'sub_category', 'model_no', 'material', 
            'sub_material', 'material_type', 'quantity', 'remark', 
            'estimate_rate', 'size', 'color',
        ]


class CreateWorkOrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    work_order_items = WorkOrderItemsSerializer(many=True, read_only=True)

    class Meta:
        model = WorkOrder
        fields = [
            'customer', 'order_no', 'remark', 'total_estimate', 
            'delivery_date', 'work_order_items'
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
    sub_material_id = serializers.CharField(source='sub_material.pk', read_only=True)
    sub_material_name = serializers.CharField(source='sub_material.name', read_only=True)
    
    class Meta:
        model = ModelNumberBasedProducts
        fields = ['model_no','category_id','sub_category_id','material_id','sub_material_id','material_type_id','color','category_name','sub_category_name','material_name','sub_material_name','material_type_name']
        
        
class ModelOrderNumbersSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ModelNumberBasedProducts
        fields = ['model_no']
        
        
class WorkOrderStaffAssignSerializer(serializers.ModelSerializer):
    staff_id = serializers.PrimaryKeyRelatedField(queryset=Staff.objects.all(), source='staff')
    staff_name = serializers.SerializerMethodField()
    work_order_status = serializers.SerializerMethodField()
    time_spent = serializers.DecimalField(max_digits=5, decimal_places=2)
    wage = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = WorkOrderStaffAssign
        fields = ['staff_id', 'staff_name', 'time_spent', 'wage', 'work_order', 'work_order_status']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        work_order = None

        # Check if 'initial_data' exists (only during deserialization)
        if hasattr(self, 'initial_data') and self.initial_data.get('work_order'):
            try:
                work_order = WorkOrder.objects.get(pk=self.initial_data['work_order'])
            except WorkOrder.DoesNotExist:
                pass

        # When using instance (e.g., during GET)
        elif self.instance:
            if isinstance(self.instance, list) and self.instance:  # many=True case
                work_order = self.instance[0].work_order
            elif hasattr(self.instance, 'work_order'):
                work_order = self.instance.work_order

        if work_order:
            status = work_order.status
            staff_queryset = Staff.objects.none()

            if status == '012':
                staff_queryset = Staff.objects.filter(
                    department__name__in=["Wood Section", "Wooden Furniture", "Wood & Joinery", "wood section"],
                    is_deleted=False
                )
            elif status == '015':
                staff_queryset = Staff.objects.filter(
                    department__name__in=["Carpentry", "carpentry"],
                    is_deleted=False
                )
            elif status == '018':
                staff_queryset = Staff.objects.filter(
                    department__name="Polishing",
                    is_deleted=False
                )
            elif status == '020':
                staff_queryset = Staff.objects.filter(
                    department__name="Glass",
                    is_deleted=False
                )
            elif status == '022':
                staff_queryset = Staff.objects.filter(
                    department__name="Packing",
                    is_deleted=False
                )

            self.fields['staff_id'].queryset = staff_queryset

    def get_staff_name(self, obj):
        return obj.staff.get_fullname()
    
    def get_work_order_status(self, obj):
        return obj.work_order.get_status_display()
    
    def create(self, validated_data):
        return WorkOrderStaffAssign.objects.create(**validated_data)
    
class StaffAssignListSerializer(serializers.ModelSerializer):
    staff_id = serializers.PrimaryKeyRelatedField(queryset=Staff.objects.all(), source='staff')
    staff_name = serializers.SerializerMethodField()
    work_order_status = serializers.SerializerMethodField()

    time_spent = serializers.DecimalField(max_digits=5, decimal_places=2)
    wage = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = WorkOrderStaffAssign
        fields = ['staff_id', 'staff_name', 'time_spent', 'wage', 'work_order', 'work_order_status']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        work_order = None

        # Check if 'initial_data' exists (only during deserialization)
        if hasattr(self, 'initial_data') and self.initial_data.get('work_order'):
            try:
                work_order = WorkOrder.objects.get(pk=self.initial_data['work_order'])
            except WorkOrder.DoesNotExist:
                pass

        # When using instance (e.g., during GET)
        elif self.instance:
            if isinstance(self.instance, list) and self.instance:  # many=True case
                work_order = self.instance[0].work_order
            elif hasattr(self.instance, 'work_order'):
                work_order = self.instance.work_order

        if work_order:
            status = work_order.status
            staff_queryset = Staff.objects.none()

            if status == '012':
                staff_queryset = Staff.objects.filter(
                    department__name__in=["Wood Section", "Wooden Furniture", "Wood & Joinery", "wood section"],
                    is_deleted=False
                )
            elif status == '015':
                staff_queryset = Staff.objects.filter(
                    department__name__in=["Carpentry", "carpentry"],
                    is_deleted=False
                )
            elif status == '018':
                staff_queryset = Staff.objects.filter(
                    department__name="Polishing",
                    is_deleted=False
                )
            elif status == '020':
                staff_queryset = Staff.objects.filter(
                    department__name="Glass",
                    is_deleted=False
                )
            elif status == '022':
                staff_queryset = Staff.objects.filter(
                    department__name="Packing",
                    is_deleted=False
                )

            self.fields['staff_id'].queryset = staff_queryset

    def get_staff_name(self, obj):
        return obj.staff.get_fullname()
    
    def get_work_order_status(self, obj):
        return obj.work_order.get_status_display()
    
    def create(self, validated_data):
        return WorkOrderStaffAssign.objects.create(**validated_data)
    
class DispatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispatch
        fields = ['work_order', 'mode', 'remark', 'reference_no', 'amount']
        extra_kwargs = {
            'work_order': {'required': False} 
        }


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'



class ModelNumberBasedProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelNumberBasedProductImages
        fields = ['id', 'model', 'image', 'remark']
        read_only_fields=['id','model']



class ModelNumberBasedProductsSerializer(serializers.ModelSerializer):
    images_set = ModelNumberBasedProductImagesSerializer(read_only=True,many=True)

    class Meta:
        model = ModelNumberBasedProducts
        fields = ['id','model_no', 'category', 'sub_category', 'material', 'sub_material', 'material_type', 'color', 'size','images_set']
        read_only_fields=['id']
