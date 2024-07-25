from django.urls import path,re_path
from . import views

app_name = 'settings'

urlpatterns = [
    re_path(r'company_details_info/(?P<pk>.*)/$', views.company_details_info, name='company_details_info'),
    re_path(r'company_details_list/$', views.company_details_list, name='company_details_list'),
    re_path(r'company_details_create/$', views.company_details_create, name='company_details_create'),
    re_path(r'company_details_edit/(?P<pk>.*)/$', views.company_details_edit, name='company_details_edit'),
    re_path(r'company_details_delete/(?P<pk>.*)/$', views.company_details_delete, name='company_details_delete'),

]

