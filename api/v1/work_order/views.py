import requests

from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.forms import formset_factory
from django.db import transaction, IntegrityError
from django.urls import reverse

from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from main.functions import decrypt_message, encrypt_message
from api.v1.authentication.functions import generate_serializer_errors, get_user_token
from work_order.views import WorkOrder
from .serializers import WorkOrderSerializer,WoodWorkAssignSerializer,CarpentarySerializer,PolishSerializer,GlassSerializer,PackingSerializer
from rest_framework.views import APIView
from django.db.models import Q
from work_order.models import WoodWorkAssign,Carpentary,Polish,Glass,Packing
from work_order.forms import WoodWorksAssignForm
from main.functions import generate_form_errors, get_auto_id

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))

def get_work_order(request,id=None):
    try:
        if id:
            queryset=WorkOrder.objects.get(id=id)
            serializer=WorkOrderSerializer(queryset)
            return Response(serializer.data)
        queryset=WorkOrder.objects.all()
        serializer=WorkOrderSerializer(queryset,many=True)
        return Response(serializer.data)
    except  Exception as e:
        print(e)
        return Response({'status': False, 'message': 'Something went wrong!'})
    
#-------------------------------wood Assign----------------------------------------------

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))

def get_work_wood_assign(request,id=None):
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
def work_order_create(request):
    """
    POST: Create a new work order with nested items and images.
    """
    if request.method == 'POST':
        # Create a new work order
        serializer = WorkOrderSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)