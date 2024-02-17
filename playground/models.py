from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import datetime, timedelta

class Order(models.Model):
    order_no = models.CharField(max_length=100)
    item_name = models.CharField(max_length=255)
    model = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    lab = models.ForeignKey('Lab', on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    warranty_period = models.IntegerField(help_text="in months")
    WARRANTY_TYPE_CHOICES = [
        ('C', 'Comprehensive'),
        ('NC', 'Non-Comprehensive'),
    ]
    warranty_type = models.CharField(max_length=2, choices=WARRANTY_TYPE_CHOICES)
    warranty_provider = models.CharField(max_length=255)
    ordered_date = models.DateField()
    installation_date = models.DateField()
    manufacturer = models.CharField(max_length=255)

    def __str__(self):
        return self.order_no

class Lab(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    lab_type = models.CharField(max_length=255)
    departments = models.ManyToManyField('Department', related_name='labs')

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class WarrantyClaim(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    part_to_replace = models.CharField(max_length=255)
    specification = models.TextField()
    price_without_gst = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quotation_status = models.CharField(max_length=20, choices=[('approved', 'Approved'), ('not_approved', 'Not Approved')])
    quotation_from_company_status = models.CharField(max_length=20, choices=[('received', 'Received'), ('not_received', 'Not Received')])
    price_with_gst = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.order.order_no} - {self.part_to_replace}"
