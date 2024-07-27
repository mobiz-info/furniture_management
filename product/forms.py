from datetime import date

from django import forms
from django.forms import formset_factory, inlineformset_factory
from django.forms.widgets import TextInput,Textarea,Select,DateInput,CheckboxInput,FileInput,PasswordInput

from . models import *


class MaterialsForm(forms.ModelForm):
    
    class Meta:
        model = Materials
        fields = ['name','is_subcategory','image']

        widgets = {
            'name': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter Material Name'}), 
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }
        

class MaterialsTypeForm(forms.ModelForm):
    sub_category_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'type': 'text','class': 'required form-control type_sub_category_name','placeholder': 'Enter Material Type Sub Category Names'}))
    
    class Meta:
        model = MaterialsType
        fields = ['name','is_subcategory','sub_category_name']

        widgets = {
            'name': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter Material Type Name'}), 
            'is_subcategory': CheckboxInput(attrs={'class': 'material_type_subcategory_checkbox'}), 
            'sub_category_name': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter Sub Category Name'}), 
        }
        
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        
        if instance and isinstance(instance, MaterialsType):
            self.fields['sub_category_name'].initial = instance.subcategories_joint()
        

class ProductCategoryForm(forms.ModelForm):
    
    class Meta:
        model = ProductCategory
        fields = ['name','is_subcategory','image']

        widgets = {
            'name': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter Product Category Name'}), 
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }
        

class ProductSubCategoryForm(forms.ModelForm):
    
    class Meta:
        model = ProductSubCategory
        fields = ['name']

        widgets = {
            'name': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter Product Sub Category Name'}), 
        }
        

class ProductForm(forms.ModelForm):
    source = forms.ChoiceField(widget=forms.RadioSelect,choices=PRODUCT_SOURCE_CHOICES)
    
    class Meta:
        model = Product
        fields = ['name','color','item_code','source','approximate_development_time','remark','feuture_image','product_category','product_sub_category','material','material_type','material_type_category']

        widgets = {
            'name': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter Product Name'}), 
            'color': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter Product Color'}), 
            'item_code': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter Item Code'}), 
            'approximate_development_time': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter Product Sub Category Name'}), 
            'feuture_image': FileInput(attrs={'class': 'form-control dropify'}),
            'product_category': Select(attrs={'class': 'select2 form-control custom-select'}),
            'product_sub_category': Select(attrs={'class': 'select2 form-control custom-select'}),
            'material': Select(attrs={'class': 'select2 form-control custom-select'}),
            'material_type': Select(attrs={'class': 'select2 form-control custom-select'}),
            'material_type_category':  Select(attrs={'class': 'select2 form-control custom-select'}),
        }
        

class ProductImageForm(forms.ModelForm):
    
    class Meta:
        model = ProductImage
        fields = ['image']

        widgets = {
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }