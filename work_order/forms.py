from django import forms
from django.forms.widgets import TextInput,Textarea,Select,DateInput,CheckboxInput,FileInput,PasswordInput,NumberInput
from django.forms import TextInput, URLInput, EmailInput
from django.forms import inlineformset_factory
from django.forms.widgets import TextInput,Textarea,Select,DateInput,CheckboxInput,FileInput,PasswordInput

from product.models import *
from customer.models import Customer
from .models import WorkOrder, WoodWorkAssign, WorkOrderItems,WorkOrderImages, Carpentary, Polish, Glass, Packing, WorkOrderStatus
from work_order.models import Color,Size,ModelNumberBasedProducts
from django.forms.widgets import SelectMultiple

class CustomerForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Customer Name'}))
    mobile_number = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Mobile No.'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Address','rows':'2'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email Id'}))
    gst_no = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter GST No.'}), required=False)

    class Meta:
        model = Customer
        fields = ['name', 'mobile_number', 'address', 'email', 'gst_no']

class DateInput(forms.DateInput):
    input_type='date'


class WorkOrderForm(forms.ModelForm):

    class Meta:
        model = WorkOrder
        fields = ['order_no','remark','total_estimate','delivery_date']
        
        widgets = {
                'order_no': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Order No','readonly': 'readonly'}),
                'remark': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Order No'}),
                'total_estimate': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Order No'}),
                'delivery_date': DateInput(attrs={'class': 'form-control', 'placeholder': 'Enter Delivery Date'}),
            }
        
class WorkOrderStatusForm(forms.ModelForm):
    
    class Meta:
        model = WorkOrderStatus
        fields = ['to_section', 'description']
        
        widgets = {
            'to_section': Select(attrs={'class': 'select2 form-control custom-select','placeholder': 'Select Status'}),
            'description': Textarea(attrs={'class': 'form-control','rows':'2'}),
        }
        
class WorkOrderItemsForm(forms.ModelForm):
    class Meta:
        model = WorkOrderItems
        fields = ['category', 'sub_category', 'model_no', 'material', 'sub_material', 'material_type', 'quantity', 'remark','estimate_rate','size','color']
        
        widgets = {
                'category': Select(attrs={'class': 'select2 form-control custom-select'}),
                'sub_category': Select(attrs={'class': 'select2 form-control custom-select'}),
                'model_no': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Model No'}),
                'material': Select(attrs={'class': 'select2 form-control custom-select'}),
                'sub_material': Select(attrs={'class': 'select2 form-control custom-select'}),
                'material_type': Select(attrs={'class': 'select2 form-control custom-select'}),
                'quantity': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Quantity'}),
                'remark': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Remark'}),
                'estimate_rate': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Estimate Rate'}),
                'size': Select(attrs={'class': 'select2 form-control custom-select'}),
                'color':Select(attrs={'class': 'select2 form-control custom-select'})
            }


class WorkOrderImagesForm(forms.ModelForm):

    class Meta:
        model = WorkOrderImages
        fields = ['image','remark']
        
        widgets = {
            'image': FileInput(attrs={'class': 'form-control '}),
            'remark': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Remark'}),
        }



class WoodWorksAssignForm(forms.ModelForm):
    
    class Meta:
        model = WoodWorkAssign
        fields = ['material', 'quality', 'quantity', 'rate']
        widgets = {
            'material':Select(attrs={'class': 'select2 form-control custom-select','placeholder': 'Select Wood'}),
            'quality': TextInput(attrs={'class': 'form-control'}),
            'quantity': NumberInput(attrs={'class': 'form-control'}),
            'rate': NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
       
WoodWorksAssignFormSet = inlineformset_factory(WorkOrder, WoodWorkAssign, form=WoodWorksAssignForm, extra=1)


class CarpentaryAssignForm(forms.ModelForm):
    
    class Meta:
        model = Carpentary
        fields = ['material', 'quality', 'quantity', 'rate']
        widgets = {
            'material':Select(attrs={'class': 'select2 form-control custom-select','placeholder': 'Select Wood'}),
            'quality': TextInput(attrs={'class': 'form-control'}),
            'quantity': NumberInput(attrs={'class': 'form-control'}),
            'rate': NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
       
CarpentaryAssignFormSet = inlineformset_factory(WorkOrder, Carpentary, form=CarpentaryAssignForm, extra=1)

class PolishAssignForm(forms.ModelForm):
    
    class Meta:
        model = Polish
        fields = ['material', 'quality', 'quantity', 'rate']
        widgets = {
            'material':Select(attrs={'class': 'select2 form-control custom-select','placeholder': 'Select Wood'}),
            'quality': TextInput(attrs={'class': 'form-control'}),
            'quantity': NumberInput(attrs={'class': 'form-control'}),
            'rate': NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
PolishAssignFormSet = inlineformset_factory(WorkOrder, Polish, form=PolishAssignForm, extra=1)

class GlassAssignForm(forms.ModelForm):
    
    class Meta:
        model = Glass
        fields = ['material', 'quality', 'quantity', 'rate']
        widgets = {
            'material':Select(attrs={'class': 'select2 form-control custom-select','placeholder': 'Select Wood'}),
            'quality': TextInput(attrs={'class': 'form-control'}),
            'quantity': NumberInput(attrs={'class': 'form-control'}),
            'rate': NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
GlassAssignFormSet = inlineformset_factory(WorkOrder, Glass, form=GlassAssignForm, extra=1)

class PackingAssignForm(forms.ModelForm):
    
    class Meta:
        model = Packing
        fields = ['material', 'quality', 'quantity', 'rate']
        widgets = {
            'material':Select(attrs={'class': 'select2 form-control custom-select','placeholder': 'Select Wood'}),
            'quality': TextInput(attrs={'class': 'form-control'}),
            'quantity': NumberInput(attrs={'class': 'form-control'}),
            'rate': NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
PackingAssignFormSet = inlineformset_factory(WorkOrder, Packing, form=PackingAssignForm, extra=1)

class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter color name', 'class': 'form-control'}),
        }


class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = ['size']
        widgets = {
            'size': forms.TextInput(attrs={'placeholder': 'Enter size', 'class': 'form-control'}),
        }


class ModelNumberBasedProductsForm(forms.ModelForm):
    class Meta:
        model = ModelNumberBasedProducts
        fields = [
            'model_no', 'category', 'sub_category', 'material', 
            'sub_material', 'material_type', 'color', 'size'
        ]
        widgets = {
            'model_no': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Model Number'}),
            'category': Select(attrs={'class': 'select2 form-control custom-select'}),
            'sub_category': Select(attrs={'class': 'select2 form-control custom-select'}),
            'material': Select(attrs={'class': 'select2 form-control custom-select'}),
            'sub_material': Select(attrs={'class': 'select2 form-control custom-select'}),
            'material_type': Select(attrs={'class': 'select2 form-control custom-select'}),
            'color': SelectMultiple(attrs={'class': 'select2-multiple form-control custom-select'}),
            'size': SelectMultiple(attrs={'class': 'select2-multiple form-control custom-select'}),
        }
