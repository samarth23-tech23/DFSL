from django import forms
from .models import Manufacturer
from .models import MainItem
from .models import Product

class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = '__all__'



class MainItemForm(forms.ModelForm):
    class Meta:
        model = MainItem
        fields = ['name', 'manufacturer']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__' 


class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'ac_no': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'pan_no': forms.TextInput(attrs={'class': 'form-control'}),
            'gst_no': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'email_id': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AddItemForm(forms.ModelForm):
    class Meta:
        model = MainItem
        fields = '__all__'  # You can specify the fields you want to include in the form here if needed