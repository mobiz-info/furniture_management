# staff/urls.py

from django.urls import re_path
from . import views
app_name = 'staff'
urlpatterns = [
    re_path(r'^department_info/(?P<pk>[0-9a-f-]+)/$', views.department_info, name='department_info'),
    re_path(r'^department_list/$', views.department_list, name='department_list'),
    re_path(r'^department_create/$', views.department_create, name='department_create'),
    re_path(r'^department_edit/(?P<pk>[0-9a-f-]+)/$', views.department_edit, name='department_edit'),
    re_path(r'^department_delete/(?P<pk>[0-9a-f-]+)/$', views.department_delete, name='department_delete'),
]
