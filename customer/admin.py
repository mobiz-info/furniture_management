from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile_number', 'email', 'date_added', 'date_updated', 'is_deleted')
    search_fields = ('name', 'mobile_number', 'email')
    list_filter = ('is_deleted', 'date_added')
