import requests

from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from product.models import Materials, ProductCategory
from main.functions import decrypt_message, encrypt_message
from api.v1.product.serializers import MaterialsSerializer, ProductCategorySerializer
from api.v1.authentication.functions import generate_serializer_errors, get_user_token
from product.views import Product
from .serializers import ProductSerializer
from rest_framework.views import APIView
from django.db.models import Q


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def materials(request):
    if request.method == 'GET':
        
        instances = Materials.objects.filter(is_deleted=False)
        serializer = MaterialsSerializer(instances,many=True)
        
        status_code = status.HTTP_200_OK
        response_data = {
            "StatusCode": 200,
            "status": status_code,
            "data": serializer.data,
        }
        
    return Response(response_data, status=status_code)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def product_category(request):
    if request.method == 'GET':
        
        instances = ProductCategory.objects.filter(is_deleted=False)
        serializer = ProductCategorySerializer(instances,many=True)
        
        status_code = status.HTTP_200_OK
        response_data = {
            "StatusCode": 200,
            "status": status_code,
            "data": serializer.data,
        }
        
    return Response(response_data, status=status_code)

@api_view(['GET'])
def get_product(request,id=None):
    try:
        if id:
            queryset=Product.objects.get(id=id)
            serializer=ProductSerializer(queryset)
            return Response(serializer.data)
        queryset=Product.objects.all()
        serializer=ProductSerializer(queryset,many=True)
        return Response(serializer.data)
    except  Exception as e:
        print(e)
        return Response({'status': False, 'message': 'Something went wrong!'})
