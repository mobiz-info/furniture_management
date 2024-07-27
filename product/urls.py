from django.urls import path,re_path
from . import views

app_name = 'product'

urlpatterns = [
    re_path(r'material-info/(?P<pk>.*)/$', views.material_info, name='material_info'),
    re_path(r'material-list/$', views.material_list, name='material_list'),
    re_path(r'create-material/$', views.create_material, name='create_material'),
    re_path(r'edit-material/(?P<pk>.*)/$', views.edit_material, name='edit_material'),
    re_path(r'delete-material/(?P<pk>.*)/$', views.delete_material, name='delete_material'),
    
    re_path(r'product-category-list/$', views.product_category_list, name='product_category_list'),
    re_path(r'create-product-category/$', views.create_product_category, name='create_product_category'),
    re_path(r'edit-product-category/(?P<pk>.*)/$', views.edit_product_category, name='edit_product_category'),
    re_path(r'delete-product-category/(?P<pk>.*)/$', views.delete_product_category, name='delete_product_category'),
    
    re_path(r'product-info/(?P<pk>.*)/$', views.product_info, name='product_info'),
    re_path(r'product-list/$', views.product_list, name='product_list'),
    re_path(r'create-product/$', views.create_product, name='create_product'),
    re_path(r'edit-product/(?P<pk>.*)/$', views.edit_product, name='edit_product'),
    re_path(r'delete-product/(?P<pk>.*)/$', views.delete_product, name='delete_product'),
    re_path(r'delete-product-image/(?P<pk>.*)/$', views.delete_product_image, name='delete_product_image'),
]


