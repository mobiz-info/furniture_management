from django import forms
from django.forms import inlineformset_factory
from .models import WoodWorkOrder, WoodWorkOrderImages, WoodWorkAssign
from customer.models import Customer
from product.models import *

class CustomerForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Customer Name'}))
    mobile_number = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Mobile No.'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Address'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email Id'}))
    gst_no = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter GST No.'}), required=False)

    class Meta:
        model = Customer
        fields = ['name', 'mobile_number', 'address', 'email', 'gst_no']


class WoodWorkOrderForm(forms.ModelForm):
    order_no = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Work Order No'}))
    category = forms.ModelChoiceField(queryset=ProductCategory.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    sub_category = forms.ModelChoiceField(queryset=ProductSubCategory.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    model_no = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Model No.'}), required=False)
    material = forms.ModelChoiceField(queryset=Materials.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    sub_material = forms.ModelChoiceField(queryset=MaterialTypeCategory.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    material_type = forms.ModelChoiceField(queryset=MaterialsType.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Quantity'}))
    delivery_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Enter Delivery Date', 'type': 'date'}))
    remark = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Remark'}), required=False)

    class Meta:
        model = WoodWorkOrder
        fields = ['order_no', 'category', 'sub_category', 'model_no', 'material', 'sub_material', 'material_type', 'quantity', 'delivery_date', 'remark']


class WoodWorkOrderImagesForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = WoodWorkOrderImages
        fields = ['image']


class WoodWorkAssignForm(forms.ModelForm):
    choose_qty = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Choose Qty'}))
    qty = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Qty'}))
    rate = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Rate'}))

    class Meta:
        model = WoodWorkAssign
        fields = ['choose_qty', 'qty', 'rate']


WoodWorkOrderImagesFormSet = inlineformset_factory(WoodWorkOrder, WoodWorkOrderImages, form=WoodWorkOrderImagesForm, extra=1)
WoodWorkAssignFormSet = inlineformset_factory(WoodWorkOrder, WoodWorkAssign, form=WoodWorkAssignForm, extra=1)
