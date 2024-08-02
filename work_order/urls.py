from django.urls import re_path
from . import views

app_name = 'work_order'

urlpatterns = [
    re_path(r'^work_order/', views.workorder, name='workorder'),
    re_path(r'^work_order_list/', views.work_order_list, name='work_order_list'),
]