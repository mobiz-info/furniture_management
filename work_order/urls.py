from django.urls import path,re_path
from . import views

app_name = 'work_order'

urlpatterns = [
    path('color-autocomplete/', views.ColorAutocomplete.as_view(), name='color_autocomplete'),
    
    re_path(r'work-order-info/(?P<pk>.*)/$', views.work_order_info, name='work_order_info'),
    re_path(r'work-order-list/$', views.work_order_list, name='work_order_list'),
    re_path(r'create-work-order/$', views.create_work_order, name='create_work_order'),
    re_path(r'edit-work-order/(?P<pk>.*)/$', views.edit_work_order, name='edit_work_order'),
    re_path(r'delete-work-order/(?P<pk>.*)/$', views.delete_work_order, name='delete_work_order'),
    re_path(r'delete-work-order-image/(?P<pk>.*)/$', views.delete_work_order_image, name='delete_work_order_image'),
    re_path(r'assign-work-order/$', views.assign_work_order, name='assign_work_order'),
    re_path(r'fetch-customer-details/$', views.fetch_customer_details, name='fetch_customer_details'),
    re_path(r'profit-loss/(?P<pk>.*)/$', views.profit_loss, name='profit_loss'),

    #-----------------Wood Section---------------------
    re_path(r'^wood_work_orders_list/', views.wood_work_orders_list, name='wood_work_orders_list'),
    re_path(r'^assign_wood/(?P<pk>.*)/$', views.assign_wood, name='assign_wood'),
    re_path(r'^allocated_wood/(?P<pk>.*)/$', views.allocated_wood, name='allocated_wood'),
    #-----------------Carpentary--------------------------
    re_path(r'^carpentary_list/', views.carpentary_list, name='carpentary_list'),
    re_path(r'^assign_carpentary/(?P<pk>.*)/$', views.assign_carpentary, name='assign_carpentary'),
    re_path(r'^allocated_carpentary/(?P<pk>.*)/$', views.allocated_carpentary, name='allocated_carpentary'),
    #-----------------Polish--------------------------
    re_path(r'^polish_list/', views.polish_list, name='polish_list'),
    re_path(r'^assign_polish/(?P<pk>.*)/$', views.assign_polish, name='assign_polish'),
    re_path(r'^allocated_polish/(?P<pk>.*)/$', views.allocated_polish, name='allocated_polish'),
    #-------------Glass/Upholstory-------------------------------------------------------
    re_path(r'^glass_list/', views.glass_list, name='glass_list'),
    re_path(r'^assign_glass/(?P<pk>.*)/$', views.assign_glass, name='assign_glass'),
    re_path(r'^allocated_glass/(?P<pk>.*)/$', views.allocated_glass, name='allocated_glass'),
    #-------------Packing-------------------------------------------------------
    re_path(r'^packing_list/', views.packing_list, name='packing_list'),
    re_path(r'^assign_packing/(?P<pk>.*)/$', views.assign_packing, name='assign_packing'),
    re_path(r'^allocated_packing/(?P<pk>.*)/$', views.allocated_packing, name='allocated_packing'),
    #--------- staff assigning for various work sections---------------------
    re_path(r'^wood_order_staff_assign/(?P<pk>.*)/$',views.wood_order_staff_assign,name='wood-order-staff-assign'),
    re_path(r'^carpentar_order_staff_assign/(?P<pk>.*)/$',views.carpentary_order_staff_assign,name='carpentar_order_staff_assign'),
    re_path(r'polish_order_staff_assign/(?P<pk>.*)/$',views.polish_order_staff_assign,name='polish_order_staff_assign'),
    re_path(r'glass_order_staff_assign/(?P<pk>.*)/$',views.glass_order_staff_assign,name='glass_order_staff_assign'),
    re_path(r'packing_order_staff_assign/(?P<pk>.*)/$',views.packing_order_staff_assign,name='packing_order_staff_assign'),
    
    re_path(r'^create_color/$', views.create_color, name='create_color'), 
    re_path(r'^color_list/$', views.color_list, name='color_list'),
    re_path(r'^delete_color/(?P<pk>.*)/$', views.delete_color, name='delete_color'),

    re_path(r'size-create/',views.size_create,name='size-create'),
    re_path(r'size-list/',views.size_list,name='size-list'),
    re_path(r'^delete-size/(?P<pk>.*)/$', views.size_delete, name='size-delete'),

    # re_path(r'model-list/',views.modelnumberbasedproducts_list,name='model-list'),
    re_path(r'model-create/',views.modelnumberbasedproducts_create,name='model-create'),
    re_path(r'model-edit/(?P<pk>.*)/$',views.modelnumberbasedproducts_update,name='model-edit'),
    re_path(r'model-delete/(?P<pk>.*)/$',views.modelnumberbasedproducts_delete,name='model-delete'),
    re_path(r'model-info/(?P<pk>.*)/$',views.modelnumberbasedproducts_info,name='model-info'),
    re_path(r'model-data/',views.get_model_details,name='model-data'),

    re_path(r'model-display/',views.modelnumberbasedproducts_card_list,name='model-display'),
    re_path(r'get-subcategories/',views.get_subcategories, name='get-subcategories'),

    re_path(r'get-subcategory/', views.get_subcategory, name='get-subcategory'),
    re_path(r'get-sub-materials/', views.get_sub_materials, name='get-sub-materials'),
    re_path(r'get-material-types/', views.get_material_types, name='get-material-types'),

    re_path(r'delete-model-image/(?P<pk>.*)/$',views.delete_model_image,name='delete-model-image'),
    re_path(r'delete-orders/',views.delete_orders,name='delete-orders'),
    
    # reports
    re_path(r'delayed-work-orders/',views.delayed_work_order_report,name='delayed_work_order_report'),

    
]
