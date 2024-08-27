# yourapp/templatetags/custom_tags.py
from collections import defaultdict
from django import template
from decimal import ROUND_DOWN, ROUND_HALF_UP, Decimal, InvalidOperation
from decimal import ROUND_DOWN, ROUND_HALF_UP, Decimal, InvalidOperation

register = template.Library()
@register.simple_tag
def multiply(value, arg):
    try:
        return value * arg
    except (ValueError, TypeError):
        return None
    
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def map(value, attr):
    return [getattr(item, attr) for item in value]

@register.filter
def multiply_and_sum(subproducts, attr):
    total = 0
    for sub in subproducts:
        unit_price = getattr(sub, attr)
        if unit_price is not None:
            total += unit_price * sub.quantity
    return total
    
# /*@register.simple_tag
# def sum_of_products(subproducts, unit_price_attr, quantity_attr):
#     total = 0
#     for subproduct in subproducts:
#         total += getattr(subproduct, str(unit_price_attr)) * getattr(subproduct, str(quantity_attr))
#     return total
    
@register.filter
def sum_of_products(queryset, field_name):
    return sum(getattr(obj, field_name) for obj in queryset)


@register.simple_tag
def multiply_and_add(unit_price, quantity, gst_value):
    try:
        total_price = Decimal(unit_price) * Decimal(quantity) + Decimal(gst_value)
        return total_price
    except (InvalidOperation, TypeError):
        return None
    
@register.filter
def calc(value, arg):
    return value * arg



# @register.filter
# def multiply_and_add_total_basic_price(subproducts_group):
#     total_basic_price = 0
#     for subproduct in subproducts_group:
#         quotationitem = subproduct.quotationitem_set.first()
#         if quotationitem:
#             total_basic_price += quotationitem.unit_price * subproduct.quantity
#     return total_basic_price

@register.filter
def multiply_and_add_total_basic_price(subproducts):
    total_price = 0
    for subproduct in subproducts:
        total_price += subproduct.quotationitem_set.first().unit_price * subproduct.quantity
    return total_price


@register.filter
def total_basic_price(subproducts):
    total_price = sum(subproduct.subproductquotationinfo.unit_price for subproduct in subproducts)
    return total_price if total_price.is_finite() else None

@register.filter
def total_price_inclusive(subproducts):
    total = sum((subproduct.subproductquotationinfo.unit_price * subproduct.quantity) + subproduct.subproductquotationinfo.gst_value for subproduct in subproducts)
    return total if total.is_finite() else None

@register.filter
def group_by_amc_provider(subproducts):
    result = {}
    for subproduct in subproducts:
        provider_name = subproduct.amc_provider
        if provider_name not in result:
            result[provider_name] = []
        result[provider_name].append(subproduct)
    return result.items()

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class":css_class})


@register.filter
def unique_amc_providers(subproducts):
    unique_providers = set()
    result = []
    for subproduct in subproducts:
        provider_name = subproduct.amc_provider.name
        if provider_name not in unique_providers:
            result.append(provider_name)
            unique_providers.add(provider_name)
    return ' व '.join(result)

@register.filter
def calc(value, arg):
    try:
        value_decimal = Decimal(value)
        arg_decimal = Decimal(arg)
        # Multiply the values
        result = value_decimal * arg_decimal
        # Round the result to the nearest integer
        result_rounded = result.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        return result_rounded
    except (InvalidOperation, TypeError):
        return None


@register.filter
def multiply_and_add(value, arg):
    return value * arg

@register.filter
def calculate_total_price(unit_price, quantity):
    try:
        unit_price_decimal = Decimal(unit_price)
        quantity_decimal = Decimal(quantity)
        total_price = unit_price_decimal * quantity_decimal
        return total_price
    except (InvalidOperation, TypeError):
        return None

@register.filter
def unique_values(queryset, field_name):
    return queryset.values_list(field_name, flat=True).distinct()


@register.filter
def group_parts_and_dates(parts_and_dates):
    grouped_parts = {}

    if not isinstance(parts_and_dates, list):
        return parts_and_dates  # Return as-is if not a list

    for item in parts_and_dates:
        if isinstance(item, tuple) and len(item) == 2:
            part, date = item
            if date in grouped_parts:
                grouped_parts[date].append(part)
            else:
                grouped_parts[date] = [part]
        else:
            grouped_parts[item] = [item]  # Handle single items

    formatted_parts_and_dates = []
    for date, parts in grouped_parts.items():
        formatted_parts_and_dates.append(f"{', '.join(parts)} - {date}")

    return ', '.join(formatted_parts_and_dates)


@register.filter(name='group_by_amc_provider')
def group_by_amc_provider(subproducts):
    if subproducts is None:
        return {}
    
    groups = {}
    for subproduct in subproducts:
        amc_provider_name = subproduct.amc_provider.name
        if amc_provider_name not in groups:
            groups[amc_provider_name] = []
        groups[amc_provider_name].append(subproduct)
    return groups.items()


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_last(value, arg):
    return value[arg-1] if value else None


@register.simple_tag
def empty_list():
    return []

@register.filter
def check_amc_provider(amc_provider, processed_providers):
    if amc_provider.id not in processed_providers:
        processed_providers.append(amc_provider.id)
        return True
    return False


@register.filter
def remove_duplicates(subproducts):
    unique_subproducts = []
    seen_main_items = set()
    seen_departments = set()

    for subproduct in subproducts:
        main_item_name = subproduct.product.main_item.name
        department_name = subproduct.product.department.name

        if main_item_name not in seen_main_items and department_name not in seen_departments:
            seen_main_items.add(main_item_name)
            seen_departments.add(department_name)
            unique_subproducts.append(subproduct)

    return unique_subproducts

@register.filter
def unique(values, key):
    seen = set()
    unique_values = []
    for value in values:
        attr = getattr(value, key)
        if attr not in seen:
            unique_values.append(value)
            seen.add(attr)
    return unique_values

@register.filter
def groupby_amc(subproducts):
    grouped = defaultdict(list)
    for subproduct in subproducts:
        grouped[subproduct.amc_provider.id].append(subproduct)
    return grouped.items()

@register.filter
def get_lab_description(lab):
    if lab and hasattr(lab, 'name'):
        lab_name = lab.name.strip().lower()
        if lab_name == "Mumbai" or lab_name == "mumbai":
            return "Directorate of Forensic Science Laboratories, Mumbai"
        else:
            return f"Regional Forensic Science Laboratory, {lab_name}"
    return "Unknown Lab"