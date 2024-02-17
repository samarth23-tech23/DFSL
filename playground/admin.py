from django.contrib import admin,messages
from django.core.exceptions import ValidationError
from django.db.models import Sum
from datetime import datetime, timedelta
from decimal import Decimal
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Order, Lab, Department, WarrantyClaim

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'item_name', 'model', 'price', 'lab', 'department',
                    'warranty_period', 'warranty_type', 'warranty_provider',
                    'ordered_date', 'installation_date', 'manufacturer')
    list_filter = ('lab', 'department', 'warranty_type')
    search_fields = ('order_no', 'item_name', 'model', 'manufacturer')
    date_hierarchy = 'ordered_date'

@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'lab_type')
    filter_horizontal = ('departments',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(WarrantyClaim)
class WarrantyClaimAdmin(admin.ModelAdmin):
    list_display = ('order', 'part_to_replace', 'specification', 'price_without_gst',
                    'quotation_status', 'quotation_from_company_status', 'price_with_gst')
    list_filter = ('quotation_status', 'quotation_from_company_status')
    search_fields = ('order__order_no', 'part_to_replace')

    def message_user(self, request, message, level=messages.INFO, extra_tags='', fail_silently=False):
        """
        Override message_user method to customize message display behavior.
        Only display the message if it is a warning or an error.
        """
        if level in [messages.WARNING, messages.ERROR]:
            super().message_user(request, message, level, extra_tags, fail_silently)

    def save_model(self, request, obj, form, change):
        warning_message = None
        if obj.quotation_status == 'approved' and obj.quotation_from_company_status == 'received':
            max_allowed_expenditure = obj.order.price * Decimal('0.20')
            current_year = datetime.now().year
            total_expenditure_in_year = WarrantyClaim.objects.filter(
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

        obj.save()

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
