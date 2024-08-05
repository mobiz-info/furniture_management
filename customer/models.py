from django.db import models
from versatileimagefield.fields import VersatileImageField
from django.contrib.auth.models import User  
from main.models import BaseModel

class Customer(BaseModel):

    name = models.CharField(max_length=255, null=False, blank=False)
    mobile_number = models.CharField(max_length=255, null=False, blank=False,unique=True)
    address = models.TextField(null=False, blank=False)
    email = models.EmailField(null=True, blank=True)
    gst_no = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_user')
    image = VersatileImageField(upload_to='customer/', null=True, blank=True)
    

    def __str__(self):
        return self.name
