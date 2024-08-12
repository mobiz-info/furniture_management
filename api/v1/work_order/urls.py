from django.urls import path, re_path
from . import views

app_name = 'api_v1_work_order'

urlpatterns = [
re_path(r'workorder-details', views.get_work_order),
]
