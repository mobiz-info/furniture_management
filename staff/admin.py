from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(Tile),
admin.site.register(Department),
admin.site.register(Designation),
admin.site.register(Attendance),



class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_fullname', 'employee_id', 'phone', 'email', 'department', 'designation','creator','auto_id')
    list_filter = ('department', 'designation')
    search_fields = ('first_name', 'last_name', 'employee_id', 'phone', 'email')
    ordering = ('-id',)
    fields = ('creator','auto_id','first_name', 'last_name', 'phone', 'address', 'email', 
              'employee_id', 'date_of_birth', 'image', 
              'user', 'department', 'designation')

admin.site.register(Staff, StaffAdmin)