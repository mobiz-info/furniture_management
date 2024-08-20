from django.urls import re_path
from . import views

app_name = 'work_order'

urlpatterns = [
    re_path(r'work-order-info/(?P<pk>.*)/$', views.work_order_info, name='work_order_info'),
    re_path(r'work-order-list/$', views.work_order_list, name='work_order_list'),
    re_path(r'create-work-order/$', views.create_work_order, name='create_work_order'),
    re_path(r'edit-work-order/(?P<pk>.*)/$', views.edit_work_order, name='edit_work_order'),
    re_path(r'delete-work-order/(?P<pk>.*)/$', views.delete_work_order, name='delete_work_order'),
    re_path(r'delete-work-order-image/(?P<pk>.*)/$', views.delete_work_order_image, name='delete_work_order_image'),
    
    #-----------------Wood Section---------------------
    re_path(r'^wood_work_orders_list/', views.wood_work_orders_list, name='wood_work_orders_list'),
    re_path(r'^assign_wood/(?P<pk>.*)/$', views.assign_wood, name='assign_wood'),
    re_path(r'^allocated_wood/(?P<pk>.*)/$', views.allocated_wood, name='allocated_wood'),
    #-----------------Carpentary--------------------------
    re_path(r'^carpentary_list/', views.carpentary_list, name='carpentary_list'),
    re_path(r'^assign_carpentary/(?P<pk>.*)/$', views.assign_carpentary, name='assign_carpentary'),
    re_path(r'^allocated_carpentary/(?P<pk>.*)/$', views.allocated_carpentary, name='allocated_carpentary'),
    #-----------------Polish--------------------------
    re_path(r'^polish_list/', views.polish_list, name='polish_list'),
    re_path(r'^assign_polish/(?P<pk>.*)/$', views.assign_polish, name='assign_polish'),
    re_path(r'^allocated_polish/(?P<pk>.*)/$', views.allocated_polish, name='allocated_polish'),
    #-------------Glass/Upholstory-------------------------------------------------------
    re_path(r'^glass_list/', views.glass_list, name='glass_list'),
    re_path(r'^assign_glass/(?P<pk>.*)/$', views.assign_glass, name='assign_glass'),
    re_path(r'^allocated_glass/(?P<pk>.*)/$', views.allocated_glass, name='allocated_glass'),
    #-------------Packing-------------------------------------------------------
    re_path(r'^packing_list/', views.packing_list, name='packing_list'),
    re_path(r'^assign_packing/(?P<pk>.*)/$', views.assign_packing, name='assign_packing'),
    re_path(r'^allocated_packing/(?P<pk>.*)/$', views.allocated_packing, name='allocated_packing'),
]
