#django
from django.db import models
#third party
from ckeditor_uploader.fields import RichTextUploadingField
from versatileimagefield.fields import VersatileImageField
#local
from main.models import BaseModel

# Create your models here.
PRODUCT_SOURCE_CHOICES = (
    ('010', 'On Product'),
    ('015', 'Other Source'),
)

class Materials(BaseModel):
    name = models.CharField(max_length=200)
    is_subcategory = models.BooleanField(default=False)
    image = VersatileImageField('Image', upload_to="product/material", blank=True, null=True)
    
    class Meta:
        db_table = 'product_material'
        verbose_name = ('Product Material')
        verbose_name_plural = ('Product Material')
        
    def __str__(self):
        return f'{self.name}'
    
    def material_types(self):
        return MaterialsType.objects.filter(is_deleted=False,material=self)
        
  
class MaterialsType(BaseModel):
    name = models.CharField(max_length=200)
    material = models.ForeignKey(Materials, on_delete=models.CASCADE)
    is_subcategory = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'product_material_type'
        verbose_name = ('Product Material Type')
        verbose_name_plural = ('Product Material Type')
        
    def __str__(self):
        return f'{self.name}'
    
    def subcategories_joint(self):
        categories = MaterialTypeCategory.objects.filter(is_deleted=False,material_type=self)
        if categories:
            return ','.join(category.name for category in categories)
        else:
            return ""
        
    def subcategories_list(self):
        return MaterialTypeCategory.objects.filter(is_deleted=False,material_type=self)
    
    
class MaterialTypeCategory(BaseModel):
    name = models.CharField(max_length=200)
    material_type = models.ForeignKey(MaterialsType, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'product_material_type_category'
        verbose_name = ('Product Material Type Category')
        verbose_name_plural = ('Product Material Type Category')
        
    def __str__(self):
        return f'{self.name}'
    

class ProductCategory(BaseModel):
    name = models.CharField(max_length=200)
    is_subcategory = models.BooleanField(default=False)
    image = VersatileImageField('Image', upload_to="product/material", blank=True, null=True)
    
    class Meta:
        db_table = 'product_category'
        verbose_name = ('Product Category')
        verbose_name_plural = ('Product Category')
        
    def __str__(self):
        return f'{self.name}'
    
    def subcategories_list(self):
        return ProductSubCategory.objects.filter(is_deleted=False,product_category=self)
   
    
class ProductSubCategory(BaseModel):
    name = models.CharField(max_length=200)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'product_sub_category'
        verbose_name = ('Product Sub Category')
        verbose_name_plural = ('Product Sub Category')
        
    def __str__(self):
        return f'{self.name}'
    

class Product(BaseModel):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=100)
    item_code = models.CharField(max_length=100)
    source = models.CharField(max_length=10, choices=PRODUCT_SOURCE_CHOICES)
    approximate_development_time = models.DecimalField(default=0,max_digits=10,decimal_places=2)
    remark = RichTextUploadingField()
    feuture_image = VersatileImageField('Image', upload_to="product/feuture_image", blank=True, null=True)
    
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    product_sub_category = models.ForeignKey(ProductSubCategory, on_delete=models.CASCADE,null=True,blank=True)
    material = models.ForeignKey(Materials, on_delete=models.CASCADE)
    material_type = models.ForeignKey(MaterialsType, on_delete=models.CASCADE,null=True,blank=True)
    material_type_category = models.ForeignKey(MaterialTypeCategory, on_delete=models.CASCADE,null=True,blank=True)
    
    class Meta:
        db_table = 'product_product'
        verbose_name = ('Product')
        verbose_name_plural = ('Product')
        
    def __str__(self):
        return f'{self.name}'
    
    
class ProductImage(BaseModel):
    image = VersatileImageField('Image', upload_to="product/product_image")
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'product_product_image'
        verbose_name = ('Product Image')
        verbose_name_plural = ('Product Image')
        
    def __str__(self):
        return f'{self.product.name}'