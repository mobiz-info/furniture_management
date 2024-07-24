from django.contrib import admin
from django.views.static import serve
from django.urls import  include, path, re_path
from core import settings
from main import views as general_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/accounts/', include('registration.backends.default.urls')),
    path('super-admin/',general_views.app,name='app'),
    path('',include(('main.urls'),namespace='main')), 
    
    # # admin panel
    path('super-admin/product/',include(('product.urls'),namespace='product')),
    # path('super-admin/sales/',include(('sales.urls'),namespace='sales')),
    # path('super-admin/staff/',include(('staff.urls'),namespace='staff')),
    # path('super-admin/branch/',include(('branch.urls'),namespace='branch')),
    # path('super-admin/payments/',include(('payments.urls'),namespace='payments')),
    # path('super-admin/core-team/',include(('core_team.urls'),namespace='core_team')),
    # path('super-admin/departments/',include(('departments.urls'),namespace='departments')),
    # path('super-admin/sales-party/',include(('sales_party.urls'),namespace='sales_party')),
    # path('super-admin/distribution/',include(('distributions.urls'),namespace='distribution')),
    # path('super-admin/office-executive/',include(('office_executive.urls'),namespace='office_executive')),
    # path('super-admin/ad-wish-hub/',include(('ad_wish_hub.urls'),namespace='ad_wish_hub')),
    # path('super-admin/file-manager/',include(('file_manager.urls'),namespace='file_manager')),
    
    # path('',include(('field_executive.urls'),namespace='field_executive')),
    # path('super-admin/field-executive/',include(('field_executive.urls'),namespace='field_executive_url')), 
    
    # re_path(r'^password-generate/(?P<employee_id>.*)/$', general_views.create_password, name='create_password'),
    # re_path(r'^password-generate-successfull/(?P<employee_id>.*)/$', general_views.password_successfull, name='password_successfull'),
    
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
]
