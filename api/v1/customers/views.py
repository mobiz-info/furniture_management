from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, renderer_classes

from customer.models import Customer
from api.v1.customers.serializers import CustomerMobileNosSerializer, CustomerSerializer

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def customer_details(request, mobile_number=None):
    try:
        if mobile_number:
            customer = Customer.objects.get(mobile_number=mobile_number)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
    except  Exception as e:
        print(e)
        return Response({'status': False, 'message': 'Something went wrong!'})
    
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def customer_mobile_nos(request):
    customer = Customer.objects.filter(is_deleted=False)
    serializer = CustomerMobileNosSerializer(customer,many=True)
    
    status_code = status.HTTP_200_OK
    response_data = {
        "StatusCode": 200,
        "status": status_code,
        "data": serializer.data,
    }
        
    return Response(response_data, status=status_code)