from django import forms
from .models import AMCProvider, Manufacturer, MainItem, Product

class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = '__all__'



class MainItemForm(forms.ModelForm):
    manufacturer = forms.ModelChoiceField(queryset=Manufacturer.objects.all(), required=False)

    class Meta:
        model = MainItem
        fields = ['name', 'manufacturer']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['expenditure_cost']
        widgets = {
            'field_name': forms.TextInput(attrs={'class': 'form-control'}),
            'another_field_name': forms.Select(attrs={'class': 'form-select'}),
            # Add more fields and their respective widgets as needed
            'expenditure_cost': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }



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

class MainItemForm(forms.ModelForm):
    manufacturer = forms.ModelChoiceField(queryset=Manufacturer.objects.all(), required=False)

    class Meta:
        model = MainItem
        fields = ['name', 'manufacturer']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'  # Corrected to use the tuple
        widgets = {
            'field_name': forms.TextInput(attrs={'class': 'form-control'}),
            'another_field_name': forms.Select(attrs={'class': 'form-select'}),
            # Add more fields and their respective widgets as needed
        }

class ItemForm(forms.ModelForm):
    manufacturer = forms.ModelChoiceField(queryset=Manufacturer.objects.all(), empty_label="Select Manufacturer")

    class Meta:
        model = MainItem
        fields = ['name', 'manufacturer']

class AddItemForm(forms.ModelForm):
    class Meta:
        model = MainItem
        fields = ['name', 'manufacturer']

class AMCProviderForm(forms.ModelForm):
    class Meta:
        model = AMCProvider
        fields = ['name', 'ac_no', 'ifsc_code', 'ac_name', 'bank_name', 'pan_no', 'state', 'pincode', 'address', 'email_id', 'contact_no']
