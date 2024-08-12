import requests

from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from main.functions import decrypt_message, encrypt_message
from api.v1.authentication.functions import generate_serializer_errors, get_user_token
from work_order.views import WorkOrder
from .serializers import WorkOrderSerializer
from rest_framework import generics
from django.db.models import Q

class WorkOrderListAPIView(generics.ListAPIView):
    queryset = WorkOrder.objects.filter(is_deleted=False).order_by('-date_added')
    serializer_class = WorkOrderSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get_queryset(self):
        query = self.request.GET.get("q")
        queryset = super().get_queryset()

        if query:
            queryset = queryset.filter(
                Q(order_no__icontains=query) |
                Q(customer__icontains=query)  # Assuming 'customer' is a searchable field
            )
        
        return queryset

