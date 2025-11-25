from django.urls import path, re_path
from . import views

app_name = 'staff'

urlpatterns = [
    re_path(r'^staff-list/$', views.staff),
    re_path(r'^staff-details/(?P<pk>.*)/$', views.staff),
    
    re_path(r'staff-attendence-list', views.staff_attendence_list),
    re_path(r'staff-attendence-choices', views.staff_attendence_choices),
    re_path(r'staff-attendence-punchin', views.staff_attendence_punchin),
    re_path(r'staff-attendence-punchout', views.staff_attendence_punchout),
]