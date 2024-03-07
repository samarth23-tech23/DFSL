from django.db import models

class Letter(models.Model):
    letter_no = models.CharField(max_length=255)
    lab_name = models.CharField(max_length=255)
    letter_date = models.DateField()

class Product(models.Model):
    letter = models.ForeignKey(Letter, on_delete=models.CASCADE, related_name='products')
    sr_no = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    buying_date = models.DateField()
    department_name = models.CharField(max_length=255)

class Subproduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='subproducts')
    type_of_part = models.CharField(max_length=255)
    part_name = models.CharField(max_length=255)
    specification = models.TextField()
    quantity = models.IntegerField()
    period_of_amc_contract = models.CharField(max_length=255)
    service_report_date = models.DateField()
    amc_provider = models.CharField(max_length=255)

      ###########
class QuotationInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField()
    ref_no = models.CharField(max_length=255)

class AMCProvider(models.Model):
    name = models.CharField(max_length=255)
    ac_no = models.CharField(max_length=255)
    ifsc_code = models.CharField(max_length=255)
    ac_name = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)
    pan_no = models.CharField(max_length=255)

class SubproductQuotationInfo(models.Model):
    quotation_info = models.ForeignKey(QuotationInfo, on_delete=models.CASCADE)
    subproduct = models.ForeignKey(Subproduct, on_delete=models.CASCADE)
    price_without_gst = models.DecimalField(max_digits=10, decimal_places=2)
    price_with_gst = models.DecimalField(max_digits=10, decimal_places=2)
    expected_delivery = models.CharField(max_length=255)
    amc_provider = models.ForeignKey(AMCProvider, on_delete=models.CASCADE)
