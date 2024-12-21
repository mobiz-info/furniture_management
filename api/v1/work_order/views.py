import requests

from django.utils.html import strip_tags
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.forms import formset_factory
from django.db import transaction, IntegrityError
from django.urls import reverse

from customer.models import Customer
from product.models import MaterialTypeCategory, Materials, MaterialsType, ProductCategory, ProductSubCategory
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, renderer_classes

from main.functions import decrypt_message, encrypt_message
from api.v1.authentication.functions import generate_serializer_errors, get_user_token
from work_order.views import WorkOrder
from .serializers import CreateWorkOrderSerializer, ModelNumberBasedProductsSerializer, ModelOrderNumbersSerializer, WorkOrderSerializer,WoodWorkAssignSerializer,CarpentarySerializer,PolishSerializer,GlassSerializer,PackingSerializer
from django.db.models import Q
from work_order.models import ModelNumberBasedProducts, WoodWorkAssign,Carpentary,Polish,Glass,Packing, WorkOrderImages, WorkOrderItems
from work_order.forms import WoodWorksAssignForm
from main.functions import generate_form_errors, get_auto_id

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))

def work_order(request,id=None):
    # try:
    if id:
        queryset=WorkOrder.objects.get(id=id)
        serializer=WorkOrderSerializer(queryset)
        return Response(serializer.data)
    queryset=WorkOrder.objects.all()
    serializer=WorkOrderSerializer(queryset,many=True)
    return Response(serializer.data)
    # except  Exception as e:
    #     print(e)
    #     return Response({'status': False, 'message': 'Something went wrong!'})
    
#-------------------------------wood Assign----------------------------------------------

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def work_wood_assign(request,id=None):
    try:
        if id:
            queryset=WoodWorkAssign.objects.get(id=id)
            serializer=WoodWorkAssignSerializer(queryset)
            return Response(serializer.data)
        queryset=WoodWorkAssign.objects.all()
        serializer=WoodWorkAssignSerializer(queryset,many=True)
        return Response(serializer.data)
    except  Exception as e:
        print(e)
        return Response({'status': False, 'message': 'Something went wrong!'})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def assign_wood_api(request, pk=None):
    try:
        if pk:
            work_order = get_object_or_404(WorkOrder, id=pk)
        else:
            return Response({
                "status": "false",
                "title": "Invalid Request",
                "message": "Work order ID is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = WoodWorkAssignSerializer(data=request.data)

        if serializer.is_valid():
            try:
                with transaction.atomic():
                        wood_assign = serializer.save(
                        work_order=work_order,
                        auto_id=get_auto_id(WoodWorkAssign),
                        creator=request.user
                    )

                work_order.status = "012"
                work_order.is_assigned = True
                work_order.save()

                    
                response_data = {
                        "status": "true",
                        "title": "Successfully Assigned",
                        "message": "Wood assigned successfully.",
                    }
                return Response(response_data, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({
                    "status": "false",
                    "title": "Failed",
                    "message": "An unexpected error occurred: " + str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                "status": "false",
                "title": "Invalid Data",
                "message": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(e)
        return Response({
            "status": "false",
            "title": "Failed",
            "message": "Something went wrong: " + str(e),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#-----------------------------------carpenter_api-------------------------------------------

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))

def carpentary_details(request,id=None):
    try:
        if id:
            queryset=Carpentary.objects.get(id=id)
            serializer=CarpentarySerializer(queryset)
            return Response(serializer.data)
        queryset=Carpentary.objects.all()
        serializer=CarpentarySerializer(queryset,many=True)
        return Response(serializer.data)
    except  Exception as e:
        print(e)
        return Response({'status': False, 'message': 'Something went wrong!'})
    

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def assign_carpentary_api(request, pk=None):
    try:
        if pk:
            work_order = get_object_or_404(WorkOrder, id=pk)
        else:
            return Response({
                "status": "false",
                "title": "Invalid Request",
                "message": "Work order ID is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = CarpentarySerializer(data=request.data)

        if serializer.is_valid():
            try:
                with transaction.atomic():
                        carpentrary_assign = serializer.save(
                        work_order=work_order,
                        auto_id=get_auto_id(Carpentary),
                        creator=request.user
                    )

                work_order.status = "015"
                work_order.is_assigned = True
                work_order.save()

                    
                response_data = {
                        "status": "true",
                        "title": "Successfully Assigned",
                        "message": "Carpentary assigned successfully.",
                    }
                return Response(response_data, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({
                    "status": "false",
                    "title": "Failed",
                    "message": "An unexpected error occurred: " + str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                "status": "false",
                "title": "Invalid Data",
                "message": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(e)
        return Response({
            "status": "false",
            "title": "Failed",
            "message": "Something went wrong: " + str(e),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#----------------------------polish-------------------------------------------------------
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))

def polish_details(request,id=None):
    try:
        if id:
            queryset=Polish.objects.get(id=id)
            serializer=PolishSerializer(queryset)
            return Response(serializer.data)
        queryset=Polish.objects.all()
        serializer=PolishSerializer(queryset,many=True)
        return Response(serializer.data)
    except  Exception as e:
        print(e)
        return Response({'status': False, 'message': 'Something went wrong!'})
    
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def assign_polish_api(request, pk=None):
    try:
        if pk:
            work_order = get_object_or_404(WorkOrder, id=pk)
        else:
            return Response({
                "status": "false",
                "title": "Invalid Request",
                "message": "Work order ID is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = PolishSerializer(data=request.data)

        if serializer.is_valid():
            try:
                with transaction.atomic():
                        polish_assign = serializer.save(
                        work_order=work_order,
                        auto_id=get_auto_id(Polish),
                        creator=request.user
                    )

                work_order.status = "018"
                work_order.is_assigned = True
                work_order.save()

                    
                response_data = {
                        "status": "true",
                        "title": "Successfully Assigned",
                        "message": " assigned successfully.",
                    }
                return Response(response_data, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({
                    "status": "false",
                    "title": "Failed",
                    "message": "An unexpected error occurred: " + str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                "status": "false",
                "title": "Invalid Data",
                "message": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(e)
        return Response({
            "status": "false",
            "title": "Failed",
            "message": "Something went wrong: " + str(e),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#-------------------------------glass_api------------------------------------------
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))

def glass_details(request,id=None):
    try:
        if id:
            queryset=Glass.objects.get(id=id)
            serializer=GlassSerializer(queryset)
            return Response(serializer.data)
        queryset=Glass.objects.all()
        serializer=GlassSerializer(queryset,many=True)
        return Response(serializer.data)
    except  Exception as e:
        print(e)
        return Response({'status': False, 'message': 'Something went wrong!'})
    

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def assign_glass_api(request, pk=None):
    try:
        if pk:
            work_order = get_object_or_404(WorkOrder, id=pk)
        else:
            return Response({
                "status": "false",
                "title": "Invalid Request",
                "message": "Work order ID is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = GlassSerializer(data=request.data)

        if serializer.is_valid():
            try:
                with transaction.atomic():
                        glass_assign = serializer.save(
                        work_order=work_order,
                        auto_id=get_auto_id(Glass),
                        creator=request.user
                    )

                work_order.status = "020"
                work_order.is_assigned = True
                work_order.save()

                    
                response_data = {
                        "status": "true",
                        "title": "Successfully Assigned",
                        "message": "Glass assigned successfully.",
                    }
                return Response(response_data, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({
                    "status": "false",
                    "title": "Failed",
                    "message": "An unexpected error occurred: " + str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                "status": "false",
                "title": "Invalid Data",
                "message": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(e)
        return Response({
            "status": "false",
            "title": "Failed",
            "message": "Something went wrong: " + str(e),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#---------------------------------packing_api----------------------------------------------   
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))

def packing_details(request,id=None):
    try:
        if id:
            queryset=Packing.objects.get(id=id)
            serializer=PackingSerializer(queryset)
            return Response(serializer.data)
        queryset=Packing.objects.all()
        serializer=PackingSerializer(queryset,many=True)
        return Response(serializer.data)
    except  Exception as e:
        print(e)
        return Response({'status': False, 'message': 'Something went wrong!'})
    

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def assign_packing_api(request, pk=None):
    try:
        if pk:
            work_order = get_object_or_404(WorkOrder, id=pk)
        else:
            return Response({
                "status": "false",
                "title": "Invalid Request",
                "message": "Work order ID is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = PackingSerializer(data=request.data)

        if serializer.is_valid():
            try:
                with transaction.atomic():
                        packing_assign = serializer.save(
                        work_order=work_order,
                        auto_id=get_auto_id(Packing),
                        creator=request.user
                    )

                work_order.status = "022"
                work_order.is_assigned = True
                work_order.save()

                    
                response_data = {
                        "status": "true",
                        "title": "Successfully Assigned",
                        "message": "Packing assigned successfully.",
                    }
                return Response(response_data, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({
                    "status": "false",
                    "title": "Failed",
                    "message": "An unexpected error occurred: " + str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                "status": "false",
                "title": "Invalid Data",
                "message": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

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
def work_order_create(request):
    """
    POST: Create a new work order with nested items and images.
    """
    if request.method == 'POST':
        data = request.data
        
        # Extract customer data
        customer_data = data.get('customer', {})
        if not customer_data:
            return Response({
                "status": "false",
                "title": "Invalid Data",
                "message": "Customer data is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create or retrieve the customer
        mobile_number = customer_data.get('mobile_number')
        if not mobile_number:
            return Response({
                "status": "false",
                "title": "Invalid Data",
                "message": "Customer mobile number is required."
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if (user_details:=User.objects.filter(username=mobile_number)).exists():
            user_details = user_details.first()
        else:
            user_details = User.objects.create_user(
                username=mobile_number,
                password=f'{customer_data.get("name")}@123',
                is_active=True,
            )

        customer_instance, created = Customer.objects.get_or_create(
            mobile_number=mobile_number,
            defaults={
                'name': customer_data.get('name'),
                'address': customer_data.get('address'),
                'email': customer_data.get('email'),
                'gst_no': customer_data.get('gst_no'),
                'auto_id': get_auto_id(Customer),
                'user': user_details,
                'creator': request.user,
            }
        )
        if created:
            group, _ = Group.objects.get_or_create(name="customer")
            customer_instance.user.groups.add(group)

        # Create WorkOrder
        try:
            work_order = WorkOrder.objects.create(
                customer=customer_instance,
                order_no=data.get('order_no'),
                remark=data.get('remark'),
                total_estimate=data.get('total_estimate'),
                delivery_date=data.get('delivery_date'),
                auto_id=get_auto_id(WorkOrder),
                creator=request.user,
            )
        except Exception as e:
            return Response({
                "status": "false",
                "title": "Creation Failed",
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create WorkOrder Items
        work_order_items = data.get('work_order_items', [])
        for item in work_order_items:
            try:
                WorkOrderItems.objects.create(
                    work_order=work_order,
                    category=ProductCategory.objects.get(pk=item.get('category')),
                    sub_category=ProductSubCategory.objects.get(pk=item.get('sub_category')),
                    model_no=item.get('model_no'),
                    material=Materials.objects.get(pk=item.get('material')),
                    sub_material=MaterialTypeCategory.objects.get(pk=item.get('sub_material')),
                    material_type=MaterialsType.objects.get(pk=item.get('material_type')),
                    quantity=item.get('quantity'),
                    estimate_rate=item.get('estimate_rate'),
                    size=item.get('size'),
                    color=item.get('color'),
                    remark=item.get('remark'),
                    auto_id=get_auto_id(WorkOrderItems),
                    creator=request.user,
                )
            except Exception as e:
                return Response({
                    "status": "false",
                    "title": "Item Creation Failed",
                    "message": str(e)
                }, status=status.HTTP_400_BAD_REQUEST)

        # Create WorkOrder Images
        work_order_images = data.get('work_order_images', [])
        for image in work_order_images:
            try:
                WorkOrderImages.objects.create(
                    work_order=work_order,
                    image=image.get('image'),
                    auto_id=get_auto_id(WorkOrderImages),
                    creator=request.user,
                )
            except Exception as e:
                return Response({
                    "status": "false",
                    "title": "Image Upload Failed",
                    "message": str(e)
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": "true",
            "title": "Work Order Created",
            "work_order_id": work_order.id
        }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def model_number_based_products(request,model_no):
    queryset=ModelNumberBasedProducts.objects.filter(model_no=model_no,is_deleted=False)
    serializer=ModelNumberBasedProductsSerializer(queryset,many=True)
    
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
def order_model_numbers(request):
    queryset=ModelNumberBasedProducts.objects.filter(is_deleted=False)
    serializer=ModelOrderNumbersSerializer(queryset,many=True)
    
    status_code = status.HTTP_200_OK
    response_data = {
        "StatusCode": 200,
        "status": status_code,
        "data": serializer.data,
    }
        
    return Response(response_data, status=status_code)