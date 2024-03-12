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


def group_by_attribute(queryset, attribute_name):
    grouped = {}
    for obj in queryset:
        attribute_value = getattr(obj, attribute_name)
        if attribute_value not in grouped:
            grouped[attribute_value] = []
        grouped[attribute_value].append(obj)
    return grouped.items()