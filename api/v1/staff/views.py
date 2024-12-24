from api.v1.authentication.serializers import StaffSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from staff.models import Staff

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
    