from django.contrib import admin
from django.views.static import serve
from django.urls import  include, path, re_path
from core import settings
from main import views as general_views

urlpatterns = [
    path('ckeditor/', include('ckeditor_uploader.urls')),   
    
    path('admin/', admin.site.urls),
    path('app/accounts/', include('registration.backends.default.urls')),
    path('super-admin/',general_views.app,name='app'),
    path('',include(('main.urls'),namespace='main')), 
    path('settings/', include('settings.urls', namespace='settings')),
    path('workorder/',include('work_order.urls',namespace='workorder')),
    
    # admin panel
    path('super-admin/product/',include(('product.urls'),namespace='product')),
    path('staff/', include('staff.urls', namespace='staff')),
    
    # api
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/auth/', include(('api.v1.authentication.urls','authentication'), namespace='api_v1_authentication')),
    path('api/v1/product/', include(('api.v1.product.urls','product'), namespace='api_v1_product')),
    path('api/v1/work-order/', include(('api.v1.work_order.urls','work_order'), namespace='api_v1_work_order')),
    path('api/v1/customer/',include(('api.v1.customers.urls','customer'),namespace='customer')),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
]
