from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django import forms
from datetime import datetime, timedelta
from decimal import Decimal
from django.http import HttpResponseRedirect
from .models import Order, Lab, Department, AMC_Claim, OrderItem, Category, Item, Manufacturer,AMC_provider

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ['item', 'quantity', 'AMC_exist', 'AMC_type', 'AMC_provider', 'warranty_exist', 'Warranty_type', 'warranty_provider']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('order_no', 'get_total_quantity', 'ordered_date')
    search_fields = ('order_no',)
    date_hierarchy = 'ordered_date'

    def get_total_quantity(self, obj):
        return sum(item.quantity for item in obj.items.all())
    get_total_quantity.short_description = 'Total Quantity'

@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name', 'address')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'lab')
    search_fields = ('name', 'lab__name')
    list_filter = ('lab',)

@admin.register(AMC_Claim)
class AMC_ClaimAdmin(admin.ModelAdmin):
    list_display = ('order', 'part_to_replace', 'specification', 'price_without_gst',
                    'quotation_status', 'quotation_from_company_status', 'price_with_gst',
                    'quotation_letter_no', 'quotation_letter_date', 'received_quotation_price', 'bank_details')
    list_filter = ('quotation_status', 'quotation_from_company_status')
    search_fields = ('order__order_no', 'part_to_replace')

    def message_user(self, request, message, level=messages.INFO, extra_tags='', fail_silently=False):
        if level in [messages.WARNING, messages.ERROR]:
            super().message_user(request, message, level=level, extra_tags=extra_tags, fail_silently=fail_silently)

    def save_model(self, request, obj, form, change):
        warning_message = None
        if obj.quotation_status == 'approved' and obj.quotation_from_company_status == 'received':
            max_allowed_expenditure = obj.order.price * Decimal('0.20')
            current_year = datetime.now().year
            total_expenditure_in_year = AMC_Claim.objects.filter(
                order=obj.order,
                order__ordered_date__year=current_year,
                order__installation_date__lte=obj.order.installation_date
            ).aggregate(Sum('price_with_gst'))['price_with_gst__sum'] or Decimal('0.00')

            if total_expenditure_in_year + obj.price_with_gst > max_allowed_expenditure:
                warning_message = "Expenditure exceeds 20% of ordered price for the year."

            warranty_end_date = obj.order.installation_date + timedelta(days=obj.order.warranty_period * 30)
            if datetime.now().date() > warranty_end_date:
                warning_message = "The warranty claim is outside the warranty period."

        if warning_message:
            self.message_user(request, warning_message, level=messages.WARNING)
            return

        super().save_model(request, obj, form, change)

    def response_post_save_add(self, request, obj):
        return self.response_post_save_change(request, obj)

    def response_post_save_change(self, request, obj):
        return super().response_post_save_change(request, obj)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        try:
            return super().change_view(request, object_id, form_url, extra_context)
        except ValidationError as e:
            messages.error(request, e)
            return HttpResponseRedirect(request.path)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

from django.contrib import admin
from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'item_code', 'serial_code', 'model', 'price', 'warranty_period', 'installation_date', 'manufacturer', 'category', 'AMC_exist', 'get_amc_type', 'warranty_exist', 'get_warranty_type', 'warranty_provider')
    search_fields = ('item_name', 'item_code', 'serial_code',)
    list_filter = ('manufacturer', 'category',)
    date_hierarchy = 'installation_date'

    def get_amc_type(self, obj):
        return obj.get_AMC_type_display()

    get_amc_type.short_description = 'AMC Type'

    def get_warranty_type(self, obj):
        return obj.get_Warranty_type_display()

    get_warranty_type.short_description = 'Warranty Type'

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj and obj.AMC_exist == 'N':
            for field in ['AMC_type', 'warranty_provider']:
                if field in fieldsets[0][1]['fields']:
                    fieldsets[0][1]['fields'].remove(field)
        if obj and obj.Warranty_exist == 'N':
            for field in ['Warranty_type', 'warranty_provider']:
                if field in fieldsets[0][1]['fields']:
                    fieldsets[0][1]['fields'].remove(field)
        return fieldsets

    def get_form(self, request, obj=None, **kwargs):
        form = super(ItemAdmin, self).get_form(request, obj, **kwargs)
        if obj and obj.AMC_exist == 'N':
            if 'AMC_type' in form.base_fields:
                del form.base_fields['AMC_type']
            if 'warranty_provider' in form.base_fields:
                del form.base_fields['warranty_provider']
        if obj and obj.Warranty_exist == 'N':
            if 'Warranty_type' in form.base_fields:
                del form.base_fields['Warranty_type']
            if 'warranty_provider' in form.base_fields:
                del form.base_fields['warranty_provider']
        return form

    class Media:
        js = ('admin/js/conditional_fields.js',)
        
@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact_no', 'email')
    search_fields = ('name', 'address', 'contact_no', 'email')


@admin.register(AMC_provider)
class AMC_providerAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact_no', 'email', 'bank_name', 'account_no', 'ifsc_code', 'branch')
    search_fields = ('name', 'address', 'contact_no', 'email', 'bank_name', 'account_no', 'ifsc_code', 'branch')
