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
    
    #-------------------------------Staff-------------------------
    re_path(r'staff_info/(?P<pk>.*)/$', views.staff_info, name='staff_info'),
    re_path(r'staff_list/$', views.staff_list, name='staff_list'),
    re_path(r'staff_create/$', views.staff_create, name='staff_create'),
    re_path(r'staff_edit/(?P<pk>.*)/$', views.staff_edit, name='staff_edit'),
    re_path(r'staff_delete/(?P<pk>.*)/$', views.staff_delete, name='staff_delete'),
    
]
