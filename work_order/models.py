# models.py in work_order app
from django.db import models
from versatileimagefield.fields import VersatileImageField
from main.models import BaseModel
from customer.models import Customer
from product.models import *
import uuid

class WoodWorkOrder(BaseModel):
    order_no = models.CharField(max_length=255, null=False, blank=False)
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(ProductSubCategory, null=True, blank=True, on_delete=models.CASCADE)
    model_no = models.CharField(max_length=255, null=True, blank=True)
    material = models.ForeignKey(Materials, on_delete=models.CASCADE)
    sub_material = models.ForeignKey(MaterialTypeCategory, null=True, blank=True, on_delete=models.CASCADE)
    material_type = models.ForeignKey(MaterialsType, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    delivery_date = models.DateField(null=False, blank=False)
    remark = models.TextField(null=True, blank=True)
    is_assigned = models.BooleanField(default=False)

    class Meta:
        db_table = 'WoodWorkOrder'

    def __str__(self):
        return f'WorkOrder {self.order_no}'


class WoodWorkOrderImages(BaseModel):
    work_order = models.ForeignKey(WoodWorkOrder, on_delete=models.CASCADE)
    image = VersatileImageField(upload_to='work_order_images/')

    class Meta:
        db_table = 'WoodWorkOrderImages'

    def __str__(self):
        return f'WorkOrderImage {self.id}'


class WoodWorkAssign(BaseModel):
    work_order = models.ForeignKey(WoodWorkOrder, on_delete=models.CASCADE)
    choose_qty = models.CharField(max_length=255)
    qty = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'WoodWorkAssign'

    def __str__(self):
        return f'WorkAssign {self.id}'
