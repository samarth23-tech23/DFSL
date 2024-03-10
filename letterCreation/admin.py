from django.contrib import admin
from .models import Letter, Product, Subproduct, QuotationInfo, AMCProvider, SubproductQuotationInfo

@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ['letter_no', 'lab_name', 'letter_date']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['sr_no', 'name', 'price', 'buying_date', 'department_name']

@admin.register(Subproduct)
class SubproductAdmin(admin.ModelAdmin):
    list_display = ['type_of_part', 'part_name', 'specification', 'quantity', 'period_of_amc_contract', 'service_report_date', 'amc_provider']

@admin.register(QuotationInfo)
class QuotationInfoAdmin(admin.ModelAdmin):
    list_display = ['subproduct', 'date', 'ref_no']

@admin.register(AMCProvider)
class AMCProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'ac_no', 'ifsc_code', 'ac_name', 'bank_name', 'pan_no', 'state', 'pincode', 'address']

@admin.register(SubproductQuotationInfo)
class SubproductQuotationInfoAdmin(admin.ModelAdmin):
    list_display = ['quotation_info', 'subproduct', 'unit_price', 'price_without_gst', 'price_with_gst', 'gst_percentage', 'gst_value', 'expected_delivery', 'amc_provider']
