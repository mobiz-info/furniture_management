from django.contrib.auth.models import User

from rest_framework import serializers
from work_order.models import *

class WorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields=['order_no','customer','status','delivery_date','total_estimate']

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