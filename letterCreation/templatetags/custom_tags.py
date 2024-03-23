# yourapp/templatetags/custom_tags.py
from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.simple_tag
def multiply(value1, value2):
    try:
        value1_decimal = Decimal(value1)
        value2_decimal = Decimal(value2)
        result = value1_decimal * value2_decimal
        return result if result.is_finite() else None
    except (InvalidOperation, TypeError):
        return None


@register.simple_tag
def multiply_and_add(unit_price, quantity, gst_value):
    try:
        total_price = Decimal(unit_price) * Decimal(quantity) + Decimal(gst_value)
        return total_price
    except (InvalidOperation, TypeError):
        return None
    
@register.filter
def total_basic_price(subproducts):
    total_price = sum(subproduct.subproductquotationinfo.unit_price for subproduct in subproducts)
    return total_price if total_price.is_finite() else None

@register.filter
def total_price_inclusive(subproducts):
    total = sum((subproduct.subproductquotationinfo.unit_price * subproduct.quantity) + subproduct.subproductquotationinfo.gst_value for subproduct in subproducts)
    return total if total.is_finite() else None


@register.filter
def groupbyamcprovider(subproducts):
    grouped = {}
    for subproduct in subproducts:
        amc_provider = subproduct.amc_provider
        if amc_provider in grouped:
            grouped[amc_provider].append(subproduct)
        else:
            grouped[amc_provider] = [subproduct]
    return grouped.items()