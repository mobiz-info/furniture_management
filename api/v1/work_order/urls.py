from django.urls import path, re_path
from . import views

app_name = 'api_v1_work_order'

urlpatterns = [
    re_path(r'workorder-details', views.get_work_order),
    re_path(r'work-assign',views.get_work_wood_assign),
    re_path(r'carpentary-details',views.carpentary_details),
    re_path(r'polish-details',views.polish_details),
]
