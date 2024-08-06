from django.contrib.auth.models import User

from rest_framework import serializers
from product.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields=['name','color','item_code','approximate_development_time','product_category','product_sub_category']


