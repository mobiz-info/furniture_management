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
    # # admin panel
    path('super-admin/product/',include(('product.urls'),namespace='product')),
    path('staff/', include('staff.urls', namespace='staff')),


    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
]
