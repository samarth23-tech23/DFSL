from django.contrib import admin
from .models import Order, Lab, Department

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
    search_fields = ('name', 'lab_type')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
