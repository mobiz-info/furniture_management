import requests
import datetime
from django.utils.html import strip_tags
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.forms import formset_factory
from django.db import transaction, IntegrityError
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from customer.models import Customer
from product.models import MaterialTypeCategory, Materials, MaterialsType, ProductCategory, ProductSubCategory
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError

from main.functions import decrypt_message, encrypt_message, safe_get_or_400
from api.v1.authentication.functions import generate_serializer_errors, get_user_token
from work_order.views import WorkOrder, WorkOrderStaffAssign
from .serializers import *
from django.db.models import Q
from work_order.models import WORK_ORDER_CHOICES, ModelNumberBasedProducts, WoodWorkAssign,Carpentary,Polish,Glass,Packing, WorkOrderImages, WorkOrderItems, WorkOrderStatus
from work_order.forms import WoodWorksAssignForm
from main.functions import generate_form_errors, get_auto_id,log_activity

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def work_order(request, id=None):
    status_value = request.query_params.get('status_value')
    auth_staff = Staff.objects.get(user=request.user)

    if id:
        try:
            queryset = WorkOrder.objects.get(id=id, is_deleted=False)
            serializer = WorkOrderSerializer(queryset)
            return Response(serializer.data)
        except WorkOrder.DoesNotExist:
            return Response({"error": "Work order not found."}, status=404)
    else:
        queryset = WorkOrder.objects.filter(is_deleted=False)
        
        if status_value:
            queryset = queryset.filter(status=status_value)

        # # Restrict access if not FRONT OFFICE or OWNER
        # if auth_staff.department.name not in ["FRONT OFFICE", "OWNER"]:
        #     assigned_work_order_ids = WorkOrderStaffAssign.objects.filter(
        #         staff=auth_staff
        #     ).values_list("work_order__pk", flat=True)
            
        #     print("staff")
        #     if assigned_work_order_ids.exists():
        #         print("exist")
        #         queryset = queryset.filter(pk__in=assigned_work_order_ids)

        serializer = WorkOrderSerializer(queryset.order_by("date_added"), many=True)
        return Response(serializer.data)


    
#-------------------------------wood Assign----------------------------------------------

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def work_assign_status(request):
    choices = [{"key": key, "value": value} for key, value in WORK_ORDER_CHOICES]
    
    status_code = status.HTTP_200_OK
    response_data = {
        "StatusCode": 200,
        "status": status_code,
        "data": choices,
    }
        
    return Response(response_data, status=status_code)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def work_order_assign(request,pk):
    work_order = WorkOrder.objects.get(pk=pk,is_deleted=False)
    serializer = WorkOrderAssignSerializer(data=request.data)
    
    if serializer.is_valid():
        data = serializer.save(
        work_order=work_order,
        auto_id=get_auto_id(WorkOrderStatus),
        creator=request.user
        )
        work_order.status = data.to_section
        work_order.save()
        log_activity(
                created_by=request.user,
                description=f"Assigned work order --'{work_order}'"
            )
        response_data = {
                "status": "true",
                "title": "Successfully Assigned",
                "message": f'Work assigned successfully completed from {data.get_from_section_display()} to {data.get_to_section_display()}.',
            }
        return Response(response_data, status=status.HTTP_200_OK)
    
    else:
        return Response({
            "status": "false",
            "title": "Invalid Data",
            "message": serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)


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
                log_activity(
                    created_by=request.user,
                    description=f"assigned wood for work order-- '{work_order}'"
                    )

                    
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
        assigned_work_order_ids = WorkOrderStaffAssign.objects.filter(staff__user=request.user).values_list("work_order__pk")
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
                log_activity(
                    created_by=request.user,
                    description=f"assigned carpentary for work order-- '{work_order}'"
                    )

                    
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
                log_activity(
                    created_by=request.user,
                    description=f"assigned polish for work order-- '{work_order}'"
                    )

                    
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
                log_activity(
                    created_by=request.user,
                    description=f"assigned glass for work order-- '{work_order}'"
                    )

                    
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
                log_activity(
                    created_by=request.user,
                    description=f"assigned packing for workorder-- '{work_order}'"
                    )

                    
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

        mobile_number = customer_data.get('mobile_number')
        if not mobile_number:
            return Response({
                "status": "false",
                "title": "Invalid Data",
                "message": "Customer mobile number is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create or retrieve the user
        if (user_details := User.objects.filter(username=mobile_number)).exists():
            user_details = user_details.first()
        else:
            user_details = User.objects.create_user(
                username=mobile_number,
                password=f'{customer_data.get("name")}@123',
                is_active=True,
            )

        # Create or retrieve the customer
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

        try:
            with transaction.atomic():
                work_order = WorkOrder.objects.create(
                    customer=customer_instance,
                    order_no=data.get('order_no'),
                    remark=data.get('remark'),
                    total_estimate=data.get('total_estimate'),
                    delivery_date=data.get('delivery_date'),
                    auto_id=get_auto_id(WorkOrder),
                    creator=request.user,
                )

                work_order_items = data.get('work_order_items', [])
                if not work_order_items:
                    return Response({
                        "status": "false",
                        "title": "Invalid Data",
                        "message": "No work order items provided."
                    }, status=status.HTTP_400_BAD_REQUEST)

                for item in work_order_items:
                    try:
                        category = safe_get_or_400(ProductCategory, item.get('category'), 'Category')
                        sub_category = safe_get_or_400(ProductSubCategory, item.get('sub_category'), 'Sub Category')
                        material = safe_get_or_400(Materials, item.get('material'), 'Material')
                        sub_material = safe_get_or_400(MaterialsType, item.get('sub_material'), 'Sub Material')
                        material_type = safe_get_or_400(MaterialTypeCategory, item.get('material_type'), 'Material Type')
                        size = safe_get_or_400(Size, item.get('size'), 'Size')
                        color = safe_get_or_400(Color, item.get('color'), 'Color')
                    except ValidationError as ve:
                        return Response({
                            "status": "false",
                            "title": "Invalid Data",
                            "message": ve.detail,
                        }, status=status.HTTP_400_BAD_REQUEST)

                    model_no = item.get('model_no')
                    estimate_rate = item.get('estimate_rate')
                    quantity = item.get('quantity')
                    remark = item.get('remark')

                    work_order_item = WorkOrderItems.objects.create(
                        work_order=work_order,
                        category=category,
                        sub_category=sub_category,
                        model_no=model_no,
                        material=material,
                        sub_material=sub_material,
                        material_type=material_type,
                        quantity=quantity,
                        estimate_rate=estimate_rate,
                        size=size,
                        color=color,
                        remark=remark,
                        auto_id=get_auto_id(WorkOrderItems),
                        creator=request.user,
                    )

                    # ModelNumberBasedProducts management
                    model_exists = ModelNumberBasedProducts.objects.filter(model_no=model_no).exists()
                    if not model_exists:
                        model_number_based_product = ModelNumberBasedProducts.objects.create(
                            auto_id=get_auto_id(ModelNumberBasedProducts),
                            creator=request.user,
                            model_no=model_no,
                            category=category,
                            sub_category=sub_category,
                            material=material,
                            sub_material=sub_material,
                            material_type=material_type,
                        )
                        model_number_based_product.color.add(color)
                        model_number_based_product.size.add(size)
                    else:
                        model_number_based_product = ModelNumberBasedProducts.objects.get(model_no=model_no)
                        model_number_based_product.color.add(color)
                        model_number_based_product.size.add(size)

                    model_number_based_product.save()

                    # (Optional) Handle images if needed in future
                    # images = item.get('work_order_images', [])
                    # for image in images:
                    #     WorkOrderImages.objects.create(
                    #         work_order=work_order_item,
                    #         image=image.get('image'),
                    #         auto_id=get_auto_id(WorkOrderImages),
                    #         creator=request.user,
                    #     )

                log_activity(
                    created_by=request.user,
                    description=f"created work order-- '{work_order}'"
                )

                return Response({
                    "status": "true",
                    "title": "Work Order Created",
                    "work_order_id": work_order.id
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "status": "false",
                "title": "Failed",
                "message": "An unexpected error occurred: " + str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


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

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def work_order_staff_assign(request, pk):
    try:
        work_order = WorkOrder.objects.get(pk=pk,is_deleted=False)
    except WorkOrder.DoesNotExist:
        return Response({
            "status": "false",
            "title": "Not Found",
            "message": "Work order not found.",
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        assignments = WorkOrderStaffAssign.objects.filter(work_order=work_order)
        serializer = StaffAssignListSerializer(assignments, many=True)
        return Response({
            "status": "true",
            "title": "Staff Assignments",
            "data": serializer.data,
        }, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data 
        if not isinstance(data, list):
            return Response({
                "status": "false",
                "title": "Invalid Data",
                "message": "Expected a list of staff assignments.",
            }, status=status.HTTP_400_BAD_REQUEST)

        errors = []
        success_count = 0

        for staff_data in data:
            serializer = WorkOrderStaffAssignSerializer(data=staff_data)
            if serializer.is_valid():
                serializer.save(
                    work_order=work_order,
                    auto_id=get_auto_id(WorkOrderStaffAssign),
                    creator=request.user
                )
                success_count += 1
            else:
                errors.append(serializer.errors)

        work_order.is_assigned = True
        work_order.save()
        log_activity(
                created_by=request.user,
                description=f"assigned staff for work order-- '{work_order}'"
            )

        return Response({
            "status": "true" if success_count > 0 else "false",
            "title": "Staff Assignments Processed",
            "message": f"{success_count} staff members assigned successfully.",
            "errors": errors if errors else None,
        }, status=status.HTTP_200_OK if success_count > 0 else status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([JSONRenderer])
def add_accessory_to_work_order(request, pk):
    try:
        work_order = WorkOrder.objects.get(pk=pk,is_deleted=False)
    except WorkOrder.DoesNotExist:
        return Response({
            "status": "false",
            "title": "Not Found",
            "message": "Work order not found.",
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        accessories = WoodWorkAssign.objects.filter(work_order=work_order)
        accessory_details = [
            {
                "material": accessory.material.name,
                "sub_material": accessory.sub_material.name if accessory.sub_material else None,
                "material_type": accessory.material_type.name if accessory.material_type else None,
                "quality": accessory.quality,
                "quantity": accessory.quantity,
                "rate": accessory.rate,
            }
            for accessory in accessories
        ]

        work_order_details = {
            "order_no": work_order.order_no,
            "customer": str(work_order.customer),
            "status": work_order.get_status_display(),
            "delivery_date": work_order.delivery_date,
            "total_estimate": work_order.total_estimate,
            "is_assigned": work_order.is_assigned,
            "accessories": accessory_details,
        }

        return Response({
            "status": "true",
            "title": "Work Order Details",
            "message": work_order_details,
        }, status=status.HTTP_200_OK)

    if request.method == 'POST':
        if work_order.status == "030":  
            return Response({
                "status": "false",
                "title": "Action Not Allowed",
                "message": "Cannot add accessories to a work order with status 'Sold'.",
            }, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        if not isinstance(data, list):
            return Response({
                "status": "false",
                "title": "Invalid Data",
                "message": "Expected a list of accessories.",
            }, status=status.HTTP_400_BAD_REQUEST)

        errors = []
        success_count = 0

        for accessory_data in data:
            serializer = WoodWorkAssignSerializer(data=accessory_data)
            if serializer.is_valid():
                try:
                    serializer.save(
                        work_order=work_order,
                        auto_id=get_auto_id(WoodWorkAssign),
                        creator=request.user
                    )
                    success_count += 1
                except Exception as e:
                    errors.append({
                        "data": accessory_data,
                        "error": str(e),
                    })
            else:
                errors.append({
                    "data": accessory_data,
                    "errors": serializer.errors,
                })

        if not work_order.is_assigned and success_count > 0:
            work_order.is_assigned = True
            work_order.save()

        return Response({
            "status": "true" if success_count > 0 else "false",
            "title": "Accessories Processed",
            "message": f"{success_count} accessories added successfully.",
            "errors": errors if errors else None,
        }, status=status.HTTP_201_CREATED if success_count > 0 else status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def dispatch_details(request, pk=None):
    try:
        if request.method == 'GET':
            if pk:
                queryset = Dispatch.objects.filter(work_order__pk=pk)
                serializer = DispatchSerializer(queryset, many=True)
            else:
                queryset = Dispatch.objects.all()
                serializer = DispatchSerializer(queryset, many=True)
            
            status_code = status.HTTP_200_OK
            response_data = {
                "StatusCode": 200,
                "status": status_code,
                "data": serializer.data,
            }
        
        elif request.method == 'POST':
            try:
                work_order = WorkOrder.objects.get(pk=pk, status="024",is_deleted=False)  
            except WorkOrder.DoesNotExist:
                return Response({
                    "StatusCode": 404,
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "WorkOrder not found",
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = DispatchSerializer(data=request.data)
            if serializer.is_valid():
                
                serializer.save(
                    work_order=work_order,
                    auto_id = get_auto_id(Dispatch),
                    creator=request.user
                )
                work_order.status = '030'  
                work_order.save()
                
                status_code = status.HTTP_201_CREATED
                response_data = {
                    "StatusCode": 201,
                    "status": status_code,
                    "message": "Dispatch details saved successfully.",
                    "data": serializer.data,
                }
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                response_data = {
                    "StatusCode": 400,
                    "status": status_code,
                    "message": "Invalid data.",
                    "errors": serializer.errors,
                }
        
        return Response(response_data, status=status_code)
    
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response_data = {
            "StatusCode": 500,
            "status": status_code,
            "message": "An error occurred.",
            "error": str(e),
        }
        return Response(response_data, status=status_code)
    

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def color_create(request):
    color_name = request.data.get('name')
    if Color.objects.filter(Q(name__iexact=color_name)).exists():

        return Response({'error': 'This color already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = ColorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        log_activity(
                created_by=request.user,
                description=f"Created colort-- '{color_name}'"
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def color_delete(request, pk):
    try:
        color = Color.objects.get(pk=pk)
    except Color.DoesNotExist:
        return Response({'error': 'Color not found.'}, status=status.HTTP_404_NOT_FOUND)

    color.delete()
    log_activity(
                created_by=request.user,
                description=f"deleted color-- '{color}'"
            )
    return Response({'message': 'Color deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def color_list(request):
    colors = Color.objects.all()
    serializer = ColorSerializer(colors, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def size_list(request):
    sizes = Size.objects.all()
    serializer = SizeSerializer(sizes, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def size_create(request):
    if request.method == 'POST':
        size_value = request.data.get('size')
        if Size.objects.filter(Q(size__iexact=size_value)).exists():
            return Response({'message': 'Size already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = SizeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            log_activity(
                created_by=request.user,
                description=f"Created size--  '{size_value}'"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def size_delete(request, pk):
    try:
        size = Size.objects.get(pk=pk)
    except Size.DoesNotExist:
        return Response({'message': 'Size not found'}, status=status.HTTP_404_NOT_FOUND)

    size.delete()
    log_activity(
                created_by=request.user,
                description=f"Size deleted-- '{size}'"
            )
    return Response({'message': 'Size deleted successfully'}, status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def modelnumberbasedproducts_list(request):
    products = ModelNumberBasedProducts.objects.all()
    paginator = PageNumberPagination()
    paginator.page_size = 10 
    paginated_products = paginator.paginate_queryset(products, request)
    serializer = ModelNumberBasedProductsSerializer(paginated_products, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def modelnumberbasedproducts_create(request):
    model_no = request.data.get('model_no')
    auto_id=get_auto_id(ModelNumberBasedProducts)
    if ModelNumberBasedProducts.objects.filter(model_no=model_no).exists():
        return Response({'message': 'Model number already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    product_serializer = ModelNumberBasedProductsSerializer(data=request.data)
    if product_serializer.is_valid():
        product = product_serializer.save(creator=request.user,auto_id=auto_id)
        images_data = request.data.get('workorderimages_set', [])
        for image_data in images_data:
            image_data['model'] = product.id
            image_serializer = ModelNumberBasedProductImagesSerializer(data=image_data)
            if image_serializer.is_valid():
                image_serializer.save(creator=request.user,auto_id=get_auto_id(ModelNumberBasedProductImages))
            else:
                product.delete()
                return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        log_activity(
                created_by=request.user,
                description=f"Created model number based product-- '{product}'"
            )
        return Response(product_serializer.data, status=status.HTTP_201_CREATED)
    return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def modelnumberbasedproducts_delete(request, pk):
    try:
        product = ModelNumberBasedProducts.objects.get(pk=pk)
    except ModelNumberBasedProducts.DoesNotExist:
        return Response({'message': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

    product.delete()
    log_activity(
                created_by=request.user,
                description=f"deleted model number based product-- '{product}'"
            )
    return Response({'message': 'Deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)



@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def modelnumberbasedproducts_update(request, pk):
    product = get_object_or_404(ModelNumberBasedProducts, pk=pk)
    product_serializer = ModelNumberBasedProductsSerializer(product, data=request.data)
    user=request.user

    if product_serializer.is_valid():
        product_serializer.save(updator=user,date_updated = datetime.datetime.now())
        
        images_data = request.data.get('workorderimages_set', [])
        for image_data in images_data:
            image_id = image_data.get('id')
            if image_id:
                # Update existing image
                image = get_object_or_404(WorkOrderImages, id=image_id, work_order=product)
                image_serializer = WorkOrderImagesSerializer(image, data=image_data)
                if image_serializer.is_valid():
                    image_serializer.save(updator=user)
                else:
                    return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Create new image
                image_data['work_order'] = product.id
                image_serializer = WorkOrderImagesSerializer(data=image_data)
                if image_serializer.is_valid():
                    image_serializer.save(creator=user)
                else:
                    return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            log_activity(
                created_by=request.user,
                description=f"Updated modelnumber based product--'{product}'"
            )
        
        return Response(product_serializer.data)
    return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def modelnumberbasedproducts_detail(request, pk):
    product = get_object_or_404(ModelNumberBasedProducts, pk=pk)
    serializer = ModelNumberBasedProductsSerializer(product)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def create_work_order_image(request, pk):
    work_order=WorkOrder.objects.get(id=pk,is_deleted=False)
    serializer = WorkOrderImagesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(
            work_order=work_order,
            auto_id=get_auto_id(WorkOrderImages),
            creator=request.user
            )
        log_activity(
                created_by=request.user,
                description=f"Created work order image for --'{work_order}'"
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)