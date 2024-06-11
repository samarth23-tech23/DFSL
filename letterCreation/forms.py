from django import forms
from .models import Manufacturer
from .models import MainItem
from .models import AMCProvider



class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = '__all__'



class MainItemForm(forms.ModelForm):
    manufacturer = forms.CharField(max_length=100)
    
    class Meta:
        model = MainItem
        fields = ['name']

class AMCProviderForm(forms.ModelForm):
    class Meta:
        model = AMCProvider
        fields = ['name', 'ac_no', 'ifsc_code', 'ac_name', 'bank_name', 'pan_no', 'state', 'pincode', 'address', 'email_id', 'contact_no']