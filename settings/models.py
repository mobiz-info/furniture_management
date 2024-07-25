from django.db import models
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
