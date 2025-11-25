from django.urls import path, re_path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index,name='index'),
    re_path(r'^mail-success/$', views.mail_success, name='mail_success'),
    
    re_path(r'^change-password/(?P<employee_id>.*)/$', views.change_password, name='change_password'),
    re_path(r'log-list/',views.processing_log_list,name='log-list'),

]



