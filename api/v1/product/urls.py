from django.urls import path, re_path
from . import views

app_name = 'api_v1_product'

urlpatterns = [
    re_path(r'^materials/$', views.materials),
    re_path(r'^product-category/$', views.product_category),
    re_path(r'product-details', views.get_product),
    
    # staff attendence ------------------------------------------
    re_path(r'staff-attendence-list', views.staff_attendence_list),
    re_path(r'staff-attendence-punchin', views.staff_attendence_punchin),
]
