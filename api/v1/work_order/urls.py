from django.urls import path, re_path
from . import views

app_name = 'api_v1_work_order'

urlpatterns = [
    re_path(r'model-no-based-products/(?P<model_no>.*)/$',views.model_number_based_products),
    re_path(r'order-model-numbers/$',views.order_model_numbers),
    
    re_path(r'workorder-details', views.work_order),
    re_path(r'create-work-orders', views.work_order_create),
    # re_path(r'workorder-details/(?P<pk>.*)/$',views.work_order),
    re_path(r'workorder-details/(?P<id>\d+)/$', views.work_order),
    
    re_path(r'work-assign-status',views.work_assign_status),
    re_path(r'work-order-assign/(?P<pk>.*)/$',views.work_order_assign),
    
    # re_path(r'wood-assign/(?P<pk>.*)/$',views.assign_wood_api),
    
    # re_path(r'carpentary-details',views.carpentary_details),
    # re_path(r'carpentary-assign/(?P<pk>.*)/$',views.assign_carpentary_api),
    
    # re_path(r'polish-details',views.polish_details),
    # re_path(r'polish-assign/(?P<pk>.*)/$',views.assign_polish_api),
    
    # re_path(r'glass-details',views.glass_details),
    # re_path(r'glass-assign/(?P<pk>.*)/$',views.assign_glass_api),
    
    # re_path(r'packing-details',views.packing_details),
    # re_path(r'packing-assign/(?P<pk>.*)/$',views.assign_packing_api),
]
