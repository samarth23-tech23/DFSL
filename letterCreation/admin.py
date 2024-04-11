from django.contrib import admin
from .models import Letter, Product, Subproduct, Quotation, AMCProvider, QuotationItem

@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ['id','letter_no', 'lab_name', 'letter_date']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sr_no', 'price', 'buying_date', 'department_name']

@admin.register(Subproduct)
class SubproductAdmin(admin.ModelAdmin):
    list_display = ['part_name','type_of_part', 'specification', 'quantity', 'period_of_amc_contract', 'service_report_date', 'amc_provider_name']

    def amc_provider_name(self, obj):
        return obj.amc_provider.name

    amc_provider_name.short_description = 'AMC Provider Name'


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ['quotation_id','product_name', 'quotation_date', 'ref_no', 'quotation_expense_criteria','total_price' ]

    def product_name(self, obj):
        return obj.product.name

    def quotation_id(self, obj):
        return obj.id

    product_name.short_description = 'Product Name'
    quotation_id.short_description = 'Quotation ID'

@admin.register(AMCProvider)
class AMCProviderAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'ac_no', 'ifsc_code', 'ac_name', 'bank_name', 'pan_no', 'state', 'pincode', 'address']

@admin.register(QuotationItem)
class QuotationItemAdmin(admin.ModelAdmin):
    list_display = ['quotation_id', 'subproduct_name', 'unit_price', 'price_without_gst', 'price_with_gst', 'gst_percentage', 'gst_value', 'expected_delivery']

    def quotation_id(self, obj):
        return obj.quotation.id

    def subproduct_name(self, obj):
        return obj.subproduct.part_name

    quotation_id.short_description = 'Quotation ID'
    subproduct_name.short_description = 'Subproduct Name'
