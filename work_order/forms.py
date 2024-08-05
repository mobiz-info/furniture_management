from django import forms
from django.forms.widgets import TextInput,Textarea,Select,DateInput,CheckboxInput,FileInput,PasswordInput,NumberInput
from django.forms import TextInput, URLInput, EmailInput
from django.forms import inlineformset_factory
from django.forms.widgets import TextInput,Textarea,Select,DateInput,CheckboxInput,FileInput,PasswordInput

from product.models import *
from customer.models import Customer
from .models import WorkOrder, WoodWorkAssign, WorkOrderImages, WorkOrderItems

class CustomerForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Customer Name'}))
    mobile_number = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Mobile No.'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Address','rows':'2'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email Id'}))
    gst_no = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter GST No.'}), required=False)

    class Meta:
        model = Customer
        fields = ['name', 'mobile_number', 'address', 'email', 'gst_no']


class WorkOrderForm(forms.ModelForm):

    class Meta:
        model = WorkOrder
        fields = ['order_no','remark','total_estimate','delivery_date']
        
        widgets = {
                'order_no': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Order No'}),
                'remark': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Order No'}),
                'total_estimate': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Order No'}),
                'delivery_date': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Delivery Date'}),
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
                'size': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Size'}),
                'color': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Color'}),
            }


class WorkOrderImagesForm(forms.ModelForm):

    class Meta:
        model = WorkOrderImages
        fields = ['image','remark']
        
        widgets = {
            'image': FileInput(attrs={'class': 'form-control dropify'}),
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
