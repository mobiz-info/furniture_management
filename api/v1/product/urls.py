from django.urls import path, re_path
from . import views

app_name = 'api_v1_product'

urlpatterns = [
    re_path(r'^materials/$', views.materials),
    
    re_path(r'^product-category/$', views.product_category),
]
