from django.urls import re_path
from . import views

app_name = 'work_order'

urlpatterns = [
    re_path(r'^work_order/', views.workorder, name='workorder'),
    re_path(r'^work_order_list/', views.work_order_list, name='work_order_list'),
    re_path(r'^wood_work_orders_list/', views.wood_work_orders_list, name='wood_work_orders_list'),
    re_path(r'^assign_wood/(?P<pk>.*)/$', views.assign_wood, name='assign_wood'),
]