from django.urls import path, re_path
from . import views

app_name = 'customer'

urlpatterns = [
    re_path(r'^customer-details/(?P<mobile_number>\w+)', views.customer_details),
]