from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify

class Manufacturer(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, default='')
    contact_no = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name


class AMC_provider(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, default='')
    contact_no = models.CharField(max_length=15)
    email = models.EmailField()
    bank_name = models.CharField(max_length=255,default='')
    account_no = models.CharField(max_length=255,default='')
    ifsc_code = models.CharField(max_length=255,default='')
    branch = models.CharField(max_length=255,default='')

    def __str__(self):
        return self.name

class Lab(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=255)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'lab',)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Item(models.Model):
    item_name = models.CharField(max_length=255)
    item_code = models.CharField(max_length=50, unique=True, default='')
    serial_code = models.CharField(max_length=50, unique=True, default='')
    model = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    warranty_period = models.IntegerField(help_text="in months")
    AMC_exist = models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No')], default='N')
    AMC_TYPE_CHOICES = [
        ('C', 'Comprehensive'),
        ('NC', 'Non-Comprehensive'),
    ]
    WARRANTY_TYPE_CHOICES = [
        ('C', 'Comprehensive'),
        ('NC', 'Non-Comprehensive'),
    ]
    AMC_type = models.CharField(max_length=2, choices=AMC_TYPE_CHOICES, blank=True, null=True)
    warranty_exist = models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No')], default='N')
    warranty_provider = models.CharField(max_length=255, blank=True, null=True)
    Warranty_type = models.CharField(max_length=2, choices=WARRANTY_TYPE_CHOICES, blank=True, null=True)
    installation_date = models.DateField()
    AMC_provider = models.ForeignKey(AMC_provider, on_delete=models.CASCADE, blank=True, null=True)

    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    def save(self, *args, **kwargs):
        if not self.item_code:
            self.item_code = slugify(self.item_name)[:50]
        if not self.serial_code:
            self.serial_code = slugify(self.item_name)[:50]
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return self.item_name

class Order(models.Model):
    order_no = models.CharField(max_length=100)
    ordered_date = models.DateField()
    items = models.ManyToManyField(Item, through='OrderItem')

    def __str__(self):
        return self.order_no

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    AMC_exist = models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No')], default='N')
    AMC_type = models.CharField(max_length=2, choices=Item.AMC_TYPE_CHOICES, blank=True, null=True)
    AMC_provider = models.ForeignKey(AMC_provider, on_delete=models.CASCADE, blank=True, null=True)
    warranty_exist = models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No')], default='N')
    Warranty_type = models.CharField(max_length=2, choices=Item.WARRANTY_TYPE_CHOICES, blank=True, null=True)
    warranty_provider = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.order.order_no} - {self.item.item_name} - {self.quantity}"


class AMC_Claim(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    part_to_replace = models.CharField(max_length=255)
    specification = models.TextField()
    price_without_gst = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quotation_status = models.CharField(max_length=20, choices=[('approved', 'Approved'), ('not_approved', 'Not Approved')])
    quotation_from_company_status = models.CharField(max_length=20, choices=[('received', 'Received'), ('not_received', 'Not Received')])
    price_with_gst = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quotation_letter_no = models.CharField(max_length=100, blank=True, null=True)
    quotation_letter_date = models.DateField(blank=True, null=True)
    received_quotation_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    bank_details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.order.order_no} - {self.part_to_replace}"

