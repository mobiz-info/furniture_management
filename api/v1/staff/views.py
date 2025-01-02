from datetime import datetime

from api.v1.staff.serializers import Staff_Attendecne_List_Serializer
from main.functions import get_auto_id
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, renderer_classes

from staff.models import ATTENDANCE_CHOICES, Attendance, Staff
from api.v1.authentication.serializers import StaffSerializer

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def staff(request,pk=None):
    many=True
    if not pk:
        queryset=Staff.objects.filter(is_deleted=False)
    else:
        many=False
        queryset=Staff.objects.get(pk=pk,is_deleted=False)
        
    serializer=StaffSerializer(queryset,many=many)
    
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
def staff_attendence_punchin(request, pk=None):
    try:
        input_data = request.data
        success_count = 0
        unsuccess_count = 0
        
        for input in input_data:
            staff_instance = Staff.objects.get(auto_id = input)
            formatted_date = current_date.strftime('%Y-%m-%d')
            existsts = Attendance.objects.filter(staff__auto_id = staff_instance.auto_id , date = formatted_date).exists()
            if existsts:
                unsuccess_count += 1
            else:
                Attendance.objects.create(
                    creator = request.user,
                    auto_id = get_auto_id(Attendance),
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