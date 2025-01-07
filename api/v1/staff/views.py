from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes, renderer_classes

from main.functions import get_auto_id
from api.v1.authentication.serializers import StaffSerializer
from staff.models import ATTENDANCE_CHOICES, Attendance, Staff
from api.v1.staff.serializers import Staff_Attendecne_List_Serializer

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def staff(request, pk=None):
    try:
        # Queryset to fetch all non-deleted staff members
        queryset = Staff.objects.filter(is_deleted=False)

        # If no 'pk' is provided, show all staff list
        if not pk:
            # Check if pagination is required (via 'page' query parameter)
            page_number = request.query_params.get('page', None)

            if not page_number:
                # No pagination, return all staff
                serializer = StaffSerializer(queryset, many=True)
                response_data = {
                    "StatusCode": 200,
                    "status": status.HTTP_200_OK,
                    "data": serializer.data,
                }
            else:
                # Pagination logic
                paginator = PageNumberPagination()
                paginator.page_size = 20  # Define page size
                paginated_queryset = paginator.paginate_queryset(queryset, request)
                serializer = StaffSerializer(paginated_queryset, many=True)
                response_data = paginator.get_paginated_response(serializer.data).data

        else:
            # If a 'pk' is provided, return the specific staff member
            staff_instance = Staff.objects.get(pk=pk, is_deleted=False)
            serializer = StaffSerializer(staff_instance)
            response_data = {
                "StatusCode": 200,
                "status": status.HTTP_200_OK,
                "data": serializer.data,
            }

        return Response(response_data, status=status.HTTP_200_OK)

    except Staff.DoesNotExist:
        return Response({
            "StatusCode": 404,
            "status": status.HTTP_404_NOT_FOUND,
            "message": "Staff not found.",
        }, status=status.HTTP_404_NOT_FOUND)
        

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def staff_attendence_choices(request):
    
    choices = [{"key": key, "value": value} for key, value in ATTENDANCE_CHOICES]
    
    status_code = status.HTTP_200_OK
    response_data = {
        "StatusCode": 200,
        "status": status_code,
        "data": choices,
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
def staff_attendence_punchin(request):
    try:
        staff_pk = request.POST.get('staff_pk')
        
        staff_instance = Staff.objects.get(pk=staff_pk)
        instances = Attendance.objects.filter(attendance='010', date=datetime.now().date(), staff=staff_instance)
                                             
        if not instances.exists():
        
            Attendance.objects.create(
                creator = request.user,
                auto_id = get_auto_id(Attendance),
                attendance = '010',
                punchin_time =  datetime.now().time(),
                date = datetime.now().date(),
                staff = staff_instance
            )
            
            response_data = {
                "status": "true",
                "title": "Successfully Assigned",
                "message": "Staff Attendence added successfully.",
            }
        else:
            instances.delete()
        
            response_data = {
                    "status": "true",
                    "title": "Successfully Removed",
                    "message": "Staff Attendence Removed successfully.",
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
def staff_attendence_punchout(request):
    try:
        staff_pk = request.POST.get('staff_pk')
        
        staff_instance = Staff.objects.get(pk=staff_pk)
        instances = Attendance.objects.filter(attendance='010', date=datetime.now().date(), staff=staff_instance)
                                             
        if instances.exists():
            
            instances.update(
                punchout_time=datetime.now().time()
            )
            
            response_data = {
                "status": "true",
                "title": "Successfully Assigned",
                "message": "Staff Punch-out added successfully.",
            }
        else:
            instances.update(
                punchout_time=""
            )
        
            response_data = {
                    "status": "true",
                    "title": "Successfully Removed",
                    "message": "Staff Punch-out Removed successfully.",
                }
        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        # print(e)
        return Response({
            "status": "false",
            "title": "Failed",
            "message": "Something went wrong: " + str(e),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)