from rest_framework import serializers
from customer . models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        
class CustomerMobileNosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['mobile_number']
