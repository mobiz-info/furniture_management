from email.headerregistry import Group
from django.contrib.auth.models import User

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
        return obj.status.display()
    
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


class WorkOrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    work_order_items = WorkOrderItemsSerializer(many=True)
    work_order_images = WorkOrderImagesSerializer(many=True, required=False)

    class Meta:
        model = WorkOrder
        fields = [
            'customer', 'order_no', 'remark', 'total_estimate', 
            'delivery_date', 'work_order_items', 'work_order_images'
        ]

    def create(self, validated_data):
        request = self.context['request']
        
        customer_data = validated_data.pop('customer')
        work_order_items_data = validated_data.pop('work_order_items')
        work_order_images_data = validated_data.pop('work_order_images', [])

        mobile_number = customer_data.get('mobile_number')
        if (customer_instance:=Customer.objects.filter(mobile_number=mobile_number)).exists():
            customer_instance = customer_data.first()
        else:
            # Create a new user for the customer
            user_data = User.objects.create_user(
                username=mobile_number,
                password=f'{customer_data.get('name')}@123',
                is_active=True,
            )

            # Add the user to the customer group
            group, created = Group.objects.get_or_create(name="customer")
            user_data.groups.add(group)
            
            customer_instance = Customer.objects.create(
            mobile_number=mobile_number,
            name=customer_data.get('name'),
            address=customer_data.get('address'),
            email=customer_data.get('email'),
            gst_no=customer_data.get('gst_no'),
            auto_id = get_auto_id(Customer),
            user = user_data,
            creator = request.user,
        )

        work_order = WorkOrder.objects.create(
            customer=customer_instance,
            auto_id = get_auto_id(WorkOrder),
            creator = request.user,
            **validated_data
            )

        for item_data in work_order_items_data:
            work_order_item = WorkOrderItems.objects.create(
                work_order=work_order,
                auto_id = get_auto_id(WorkOrderItems),
                creator = request.user,
                **item_data
                )

            if not ModelNumberBasedProducts.objects.filter(model_no=work_order_item.model_no).exists():
                ModelNumberBasedProducts.objects.create(
                    auto_id=get_auto_id(ModelNumberBasedProducts),
                    creator=request.user,
                    model_no=work_order_item.model_no,
                    category=work_order_item.category,
                    sub_category=work_order_item.sub_category,
                    material=work_order_item.material,
                    sub_material=work_order_item.sub_material,
                    material_type=work_order_item.material_type,
                    color=work_order_item.color,
                )

        for image_data in work_order_images_data:
            WorkOrderImages.objects.create(
                work_order=work_order, 
                auto_id=get_auto_id(WorkOrderImages),
                creator=request.user,
                **image_data
                )

        return work_order