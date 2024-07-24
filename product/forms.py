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
    
    class Meta:
        model = MaterialsType
        fields = ['name','is_subcategory']

        widgets = {
            'name': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter Material Type Name'}), 
        }
        

class MaterialTypeCategoryForm(forms.ModelForm):
    
    class Meta:
        model = MaterialTypeCategory
        fields = ['name']

        widgets = {
            'name': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter Material Type Category Name'}), 
        }
    
MaterialTypeFormset = inlineformset_factory(Materials, MaterialsType, form=MaterialsTypeForm, extra=1, can_delete=True)
MaterialTypeCategoryFormset = inlineformset_factory(MaterialsType, MaterialTypeCategory, form=MaterialTypeCategoryForm, extra=1, can_delete=True)

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
    
    class Meta:
        model = Product
        fields = ['name','color','item_code','source','approximate_development_time','remark','feuture_image','product_category','product_sub_category','material','material_type','material_type_category']

        widgets = {
            'name': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter Product Name'}), 
            'color': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter Product Color'}), 
            'item_code': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter Item Code'}), 
            # 'source': 
            'approximate_development_time': TextInput(attrs={'type':'text','class': 'required form-control','placeholder' : 'Enter Product Sub Category Name'}), 
            'remark': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Remark'}), 
            'feuture_image': FileInput(attrs={'class': 'form-control dropify'}),
            'product_category': Select(attrs={'class': 'select2 form-control mb-3 custom-select'}),
            'product_sub_category': Select(attrs={'class': 'select2 form-control mb-3 custom-select'}),
            'material': Select(attrs={'class': 'select2 form-control mb-3 custom-select'}),
            'material_type': Select(attrs={'class': 'select2 form-control mb-3 custom-select'}),
            'material_type_category':  Select(attrs={'class': 'select2 form-control mb-3 custom-select'}),
        }
        

class ProductImageForm(forms.ModelForm):
    
    class Meta:
        model = ProductImage
        fields = ['image']

        widgets = {
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }