from django.urls import path, re_path
from . import views

app_name = 'staff'

urlpatterns = [
    re_path(r'^staff-list/$', views.staff),
    re_path(r'^staff-details/(?P<pk>.*)/$', views.staff),
]