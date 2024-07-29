from django.db import models
from django.contrib.auth.models import User

from versatileimagefield.fields import VersatileImageField

from main.models import BaseModel

class CompanyDetails(BaseModel): 
    name = models.CharField(max_length=255, blank=False)
    address = models.TextField(blank=False)
    location = models.CharField(max_length=255, blank=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    image = VersatileImageField(upload_to='company_images/', blank=True, null=True)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='branch_user')

    def __str__(self):
        return self.name