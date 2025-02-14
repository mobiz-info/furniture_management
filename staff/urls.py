from django.urls import re_path
from . import views

app_name = 'staff'

urlpatterns = [
    # Tile URL patterns
    re_path(r'^tile_info/(?P<pk>.*)/$', views.tile_info, name='tile_info'),
    re_path(r'^tile_list/$', views.tile_list, name='tile_list'),
    re_path(r'^tile_create/$', views.tile_create, name='tile_create'),
    re_path(r'^tile_edit/(?P<pk>.*)/$', views.tile_edit, name='tile_edit'),
    re_path(r'^tile_delete/(?P<pk>.*)/$', views.tile_delete, name='tile_delete'),
    
    re_path(r'^department_info/(?P<pk>.*)/$', views.department_info, name='department_info'),
    re_path(r'^department_list/$', views.department_list, name='department_list'),
    re_path(r'^department_create/$', views.department_create, name='department_create'),
    re_path(r'^department_edit/(?P<pk>.*)/$', views.department_edit, name='department_edit'),
    re_path(r'^department_delete/(?P<pk>.*)/$', views.department_delete, name='department_delete'),

    # Destination URL patterns
    re_path(r'^designation_info/(?P<pk>.*)/$', views.designation_info, name='designation_info'),
    re_path(r'^designation_list/$', views.designation_list, name='designation_list'),
    re_path(r'^designation_create/$', views.designation_create, name='designation_create'),
    re_path(r'^designation_edit/(?P<pk>.*)/$', views.designation_edit, name='designation_edit'),
    re_path(r'^designation_delete/(?P<pk>.*)/$', views.designation_delete, name='designation_delete'),
    
    #-------------------------------Staff-------------------------
    re_path(r'staff_info/(?P<pk>.*)/$', views.staff_info, name='staff_info'),
    re_path(r'staff_list/$', views.staff_list, name='staff_list'),
    re_path(r'staff_create/$', views.staff_create, name='staff_create'),
    re_path(r'staff_edit/(?P<pk>.*)/$', views.staff_edit, name='staff_edit'),
    re_path(r'staff_delete/(?P<pk>.*)/$', views.staff_delete, name='staff_delete'),
    
    #------------------------------- Attendence -------------------------
    re_path(r'attendence_list/$', views.attendence_list, name='attendence_list'),
    re_path(r'attendence_create/$', views.attendence_create, name='attendence_create'),
    re_path(r'attendence_edit/(?P<pk>.*)/$', views.attendence_edit, name='attendence_edit'),
    re_path(r'attendance_delete/(?P<pk>.*)/$', views.attendance_delete, name='attendance_delete'),
    
    re_path(r'get_staffs', views.get_staffs, name='get_staffs'),
    re_path(r'add_staff_to_list', views.add_staff_to_list, name='add_staff_to_list'),
    re_path(r'adding_attendence', views.adding_attendence, name='adding_attendence'),
]
