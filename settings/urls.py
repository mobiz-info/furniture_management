from django.urls import path,re_path
from . import views

app_name = 'settings'

urlpatterns = [
    re_path(r'company_details_info/(?P<pk>.*)/$', views.company_details_info, name='company_details_info'),
    re_path(r'company_details_list/$', views.company_details_list, name='company_details_list'),
    re_path(r'company_details_create/$', views.company_details_create, name='company_details_create'),
    re_path(r'company_details_edit/(?P<pk>.*)/$', views.company_details_edit, name='company_details_edit'),
    re_path(r'company_details_delete/(?P<pk>.*)/$', views.company_details_delete, name='company_details_delete'),
     
    #-----------------------Contact -----------------------------------------------
    re_path(r'contact_info/(?P<pk>.*)/$', views.contact_info, name='contact_info'),
    re_path(r'contact_list/$', views.contact_list, name='contact_list'),
    re_path(r'create_contact/$', views.create_contact, name='create_contact'),
    re_path(r'edit_contact/(?P<pk>.*)/$', views.edit_contact, name='edit_contact'),
    re_path(r'delete_contact/(?P<pk>.*)/$', views.delete_contact, name='delete_contact'),
]

