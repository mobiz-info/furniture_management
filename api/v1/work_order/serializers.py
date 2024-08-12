from django.contrib.auth.models import User

from rest_framework import serializers
from work_order.models import WorkOrder

class WorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields=['order_no','customer','status','delivery_date','total_estimate']

