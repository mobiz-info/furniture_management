from django.urls import path, re_path
from . import views

app_name = 'api_v1_work_order'

urlpatterns = [
    re_path(r'workorder-details', views.get_work_order),
    re_path(r'work-assign',views.get_work_wood_assign),
    re_path(r'wood-assign/(?P<pk>[0-9a-f-]+)/$',views.assign_wood_api),
    re_path(r'carpentary-details',views.carpentary_details),
    re_path(r'polish-details',views.polish_details),
    re_path(r'glass-details',views.glass_details),
    re_path(r'packing-details',views.packing_details),
]
