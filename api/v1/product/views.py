import requests
from datetime import datetime

from django.utils.html import strip_tags
from django.db.models import Q,Sum,Min,Max 
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAuthenticatedOrReadOnly

from .serializers import *
from product.views import Product
from product.models import Materials, ProductCategory
from main.functions import decrypt_message, encrypt_message
from api.v1.product.serializers import MaterialsSerializer, ProductCategorySerializer
from api.v1.authentication.functions import generate_serializer_errors, get_user_token


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

#  ----------------------- Staff attendence -----------------

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def staff_attendence_list(request):
    
    if request.method == 'GET':
        current_date = datetime.now()
        formatted_date = current_date.strftime('%Y-%m-%d')
        instances = Attendance.objects.filter(is_deleted=False, date = formatted_date)
        serializer = Staff_Attendecne_List_Serializer(instances, many=True)
        
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
def staff_attendence_list(request):
    
    if request.method == 'GET':
        current_date = datetime.now()
        formatted_date = current_date.strftime('%Y-%m-%d')
        instances = Attendance.objects.filter(is_deleted=False, date = formatted_date)
        serializer = Staff_Attendecne_List_Serializer(instances, many=True)
        
        status_code = status.HTTP_200_OK
        response_data = {
            "StatusCode": 200,
            "status": status_code,
            "data": serializer.data,
        }
        
    return Response(response_data, status=status_code)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def staff_attendence_punchin(request, pk=None):
    try:
        input_data = request.data
        success_count = 0
        unsuccess_count = 0
        
        for input in input_data:
            staff_instance = Staff.objects.get(auto_id = input)
            max_attendence = Attendance.objects.aggregate(Max('auto_id'))['auto_id__max']
            max_attendence = 0 if max_attendence == None else max_attendence
            current_date = datetime.now()
            formatted_date = current_date.strftime('%Y-%m-%d')
            existsts = Attendance.objects.filter(staff__auto_id = staff_instance.auto_id , date = formatted_date).exists()
            if existsts:
                unsuccess_count += 1
            else:
                Attendance.objects.create(
                    creator = request.user,
                    auto_id = int(max_attendence) + 1,
                    attendance = '010',
                    punchin_time =  datetime.now().time(),
                    date = datetime.now().date(),
                    staff = staff_instance
                )
                success_count += 1
        
        if len(input_data) == (success_count + unsuccess_count):
            response_data = {
                    "status": "true",
                    "title": "Successfully Assigned",
                    "message": "Staff Attendence added successfully.",
                }
            return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        # print(e)
        return Response({
            "status": "false",
            "title": "Failed",
            "message": "Something went wrong: " + str(e),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def staff_attendence_punchout(request, pk=None):
    try:
        input_data = request.data
        success_count = 0
        unsuccess_count = 0
        
        for input in input_data:
            staff_instance = Staff.objects.get(auto_id=input)
            current_date = datetime.now().strftime('%Y-%m-%d')
            
            try:
                attendance_entry = Attendance.objects.get(
                    staff__auto_id=staff_instance.auto_id, 
                    date=current_date
                )
                
                if attendance_entry.punchout_time is None:
                    attendance_entry.punchout_time = datetime.now().time()
                    attendance_entry.save()
                    success_count += 1
                else:
                    unsuccess_count += 1  
                
            except Attendance.DoesNotExist:
                unsuccess_count += 1 
        
        if len(input_data) == (success_count + unsuccess_count):
            response_data = {
                "status": "true",
                "title": "Punch-Out Completed",
                "message": f"Successfully punched out {success_count} staff. {unsuccess_count} could not be punched out.",
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            "status": "false",
            "title": "Failed",
            "message": "Something went wrong: " + str(e),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)