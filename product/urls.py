from django.urls import path,re_path
from . import views

app_name = 'product'

urlpatterns = [
    re_path(r'material-info/(?P<pk>.*)/$', views.material_info, name='material_info'),
    re_path(r'material-list/$', views.material_list, name='material_list'),
    re_path(r'create-material/$', views.create_material, name='create_material'),
]


