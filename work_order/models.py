import uuid

from django.db import models

from versatileimagefield.fields import VersatileImageField

from main.models import BaseModel
from customer.models import Customer
from product.models import *

WORK_ORDER_CHOICES = (
    ('010', 'New'),
    ('012', 'Wood Section'),
    ('015', 'Carperntry'),
    ('018', 'Polishing'),
    ('020', 'Glass/Upholstory'),
    ('022', 'Packing'),
    ('024', 'Dispatch'),
    ('028', 'Other Works'),
)

class ModelNumberBasedProducts(BaseModel):
    model_no = models.CharField(max_length=255)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(ProductSubCategory, null=True, blank=True, on_delete=models.CASCADE)
    material = models.ForeignKey(Materials, on_delete=models.CASCADE)
    sub_material = models.ForeignKey(MaterialTypeCategory, null=True, blank=True, on_delete=models.CASCADE)
    material_type = models.ForeignKey(MaterialsType, null=True, blank=True, on_delete=models.CASCADE)
    color = models.CharField(max_length=100,null=True, blank=True)

    class Meta:
        db_table = 'ModelNumberBasedProducts'

    def __str__(self):
        return f'{self.id}'


class WorkOrder(BaseModel):
    order_no = models.CharField(max_length=255, null=False, blank=False)
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    remark = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=3, choices=WORK_ORDER_CHOICES, default="010")
    delivery_date = models.DateField(null=False, blank=False)
    total_estimate = models.DecimalField(decimal_places=2,max_digits=20,default=0)

    class Meta:
        db_table = 'WoodWorkOrder'

    def __str__(self):
        return f'WorkOrder {self.order_no}'

    
class WorkOrderItems(BaseModel):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(ProductSubCategory, null=True, blank=True, on_delete=models.CASCADE)
    material = models.ForeignKey(Materials, on_delete=models.CASCADE)
    sub_material = models.ForeignKey(MaterialTypeCategory, null=True, blank=True, on_delete=models.CASCADE)
    material_type = models.ForeignKey(MaterialsType, null=True, blank=True, on_delete=models.CASCADE)
    model_no = models.CharField(max_length=255, null=True, blank=True)
    size = models.CharField(max_length=100,null=True, blank=True)
    remark = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=100,null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    estimate_rate = models.DecimalField(decimal_places=2,max_digits=20,default=0)

    class Meta:
        db_table = 'WorkOrderItems'

    def __str__(self):
        return f'Work Order {self.work_order.order_no}'


class WorkOrderImages(BaseModel):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    image = VersatileImageField(upload_to='work_order_images')
    remark = models.CharField(max_length=100,null=True, blank=True)

    class Meta:
        db_table = 'WorkOrderImages'

    def __str__(self):
        return f'WorkOrderImage {self.work_order.order_no}'


class WoodWorkAssign(BaseModel):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    material = models.ForeignKey(Materials, on_delete=models.CASCADE)
    sub_material = models.ForeignKey(MaterialTypeCategory, null=True, blank=True, on_delete=models.CASCADE)
    material_type = models.ForeignKey(MaterialsType, null=True, blank=True, on_delete=models.CASCADE)
    quality = models.CharField(max_length=255)
    quantity = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'WoodWorkAssign'

    def __str__(self):
        return f'WorkAssign {self.work_order.order_no}'
