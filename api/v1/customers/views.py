from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from customer.models import Customer
from api.v1.customers.serializers import CustomerSerializer

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