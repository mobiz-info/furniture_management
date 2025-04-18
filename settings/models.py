from django.db import models
from django.contrib.auth.models import User

from versatileimagefield.fields import VersatileImageField
from staff.models import *
from main.models import BaseModel
from staff.models import Designation


class CompanyDetails(BaseModel): 
    MODE_CHOICES = [
        ('subscriptions', 'Subscriptions'),
        ('amc', 'AMC'),
    ]
    
    name = models.CharField(max_length=255, blank=False)
    address = models.TextField(blank=False)
    gst = models.CharField(max_length=50, blank=False)
    concerned_staff = models.CharField(max_length=255)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, limit_choices_to={'is_deleted': False})
    mobile = models.CharField(max_length=15)
    email = models.EmailField(blank=False, unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)

    def __str__(self):
        return str(self.name)
   
    class Meta:
        verbose_name = "Company Detail"
        verbose_name_plural = "Company Details"
        
class Contact(BaseModel):
    phone = models.CharField(max_length=15)
    instagram_url = models.URLField(blank=False, null=False)
    facebook_url = models.URLField(blank=True, null=True)
    gmail = models.EmailField()
    
    def __str__(self):
        return str(self.phone)

    class Meta:
        db_table = 'contact'  
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

class Branch(BaseModel):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    image = VersatileImageField(upload_to='branches/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_deleted': False}, related_name='branch_user')

    def __str__(self):
        return self.name
    

class PermissionSet(BaseModel):
    TAB_CHOICES = [
        ('WOOD_SECTION', 'Wood Section'),
        ('GLASS/UPHOLSTORY_SECTION', 'Glass/Upholstory Section'),
        ('CARPENTARY', 'Carpentary'),
        ('POLISH', 'Polish'),
        ('PACKING', 'Packing')
    ]

    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.CASCADE, limit_choices_to={'is_deleted': False})
    tabs =models.CharField(max_length=255)

    def __str__(self):
        return f'{self.department.name}'
