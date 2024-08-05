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
]