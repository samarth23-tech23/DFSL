from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Letter, Product, Subproduct, Quotation, AMCProvider, QuotationItem
from itertools import groupby
from django.db import models

def index(request):
    return render(request,'index.html')

def load_form(request):
    return render(request,'form1.html')


def product_list(request):
    letters = Letter.objects.all()
    return render(request, 'table.html', {'letters': letters})

def letter_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    letter_id = product.letter_id
    subproducts = product.subproducts.all()
    return render(request, 'letter1.html', {'product': product,'subproducts':subproducts, 'letter_id':letter_id})

def quotation_form(request):
    letters = Letter.objects.all()
    return render(request, 'letter_intermidiate.html', {'letters': letters})

def quotation_page(request, product_id):
    product = Product.objects.get(pk=product_id)
    subproducts = product.subproducts.all()
    amc_providers_exist = set(AMCProvider.objects.values_list('name', flat=True))
    return render(request, 'quotation_info.html', {'product': product, 'subproducts': subproducts, 'amc_providers_exist': amc_providers_exist})



def product_list4(request):
    letters = Letter.objects.all()
    return render(request, 'table2.html', {'letters': letters})

def letter_detail4(request, subproduct_id):
    subproduct = Subproduct.objects.get(pk=subproduct_id)
    product = subproduct.product
    letter = product.letter
    amc_provider = subproduct.amc_provider
    related_subproducts = Subproduct.objects.filter(product=product, amc_provider=amc_provider)
    service_report_date = subproduct.service_report_date
    return render(request, 'letter4.html', {'product': product, 'amc_provider': amc_provider, 'related_subproducts': related_subproducts, 'service_report_date': service_report_date,'letter':letter})





from decimal import Decimal

def letter_detail6(request, subproduct_id):
    subproduct = Subproduct.objects.get(pk=subproduct_id)
    product = subproduct.product
    amc_provider = subproduct.amc_provider
    subproducts = Subproduct.objects.filter(product=product).select_related('amc_provider')
    quotations = Quotation.objects.filter(product=product, quotationitem__subproduct=subproduct)

    # Calculate global variables
    global_total_basic_price = Decimal('0')
    global_gst_value = Decimal('0')
    global_total_price_inclusive = Decimal('0')

    # Group subproducts by amc_provider name
    grouped_subproducts = {}
    for sub in subproducts:
        provider_name = sub.amc_provider.name
        if provider_name not in grouped_subproducts:
            grouped_subproducts[provider_name] = []
        grouped_subproducts[provider_name].append(sub)

        # Calculate total basic price, GST value, and total price inclusive
        total_basic_price = sub.quotationitem_set.first().unit_price * sub.quantity
        gst_value = total_basic_price * Decimal('0.18')
        total_price_inclusive = total_basic_price + gst_value

        # Update global variables
        global_total_basic_price += total_basic_price
        global_gst_value += gst_value
        global_total_price_inclusive += total_price_inclusive

    # Load the text based on the quotation_expense_criteria value from Quotation model
    quotation_expense_criteria_text = ""
    for quotation in quotations:
        if quotation.quotation_expense_criteria == '20%':
            quotation_expense_criteria_text = "शासन निर्णय, वित्त विभाग, क्रमांकः विअप्र-२०१३/प्र.क.३०/२०१३/विनियम, दिनांक १७ एप्रिल , २०१५ अन्वये भाग पहिला उपविभाग. २ अनुक्रमांक. ५ नियम क्र.७ यंत्राच्या कार्यसज्जतेसाठी लागणारे सुटे भाग, उपसाधने व इतर वस्तू साधनसामग्री विकत घेण्यासाठी मंजूरी देणे करिता यंत्र सामग्रीच्या पुस्तकी किमतीच्या २०% मर्यादेपर्यंत विभाग प्रमुख व प्रादेशिक कार्यालय प्रमुख यांना दरपत्रक मागून सुट्ट्या भागांची खरेदी करण्याबाबत अधिकार आहेत."
        elif quotation.quotation_expense_criteria == '25%':
            quotation_expense_criteria_text = "शासन निर्णय, वित्त विभाग, क्रमांकः विअप्र-२०१३/प्र.क.३०/२०१३/विनियम, दिनांक १७ एप्रिल , २०१५ अन्वये भाग पहिला उपविभाग. २ अनुक्रमांक. ५ नियम क्र.७ यंत्राच्या कार्यसज्जतेसाठी लागणारे सुटे भाग, उपसाधने व इतर वस्तू साधनसामग्री विकत घेण्यासाठी मंजूरी देणे करितासंयत्रे , यंत्रसामग्री आणि साधनसामग्री इत्यादीच्या दुरुस्ती करिता वार्षिक खर्च यंत्रसामग्रीच्या पुस्तकी किंमतीच्या 25% मर्यादेपर्यंत विभाग प्रमुख व प्रादेशिक कार्यालय प्रमुख यांना दरपत्रक मागून सुट्ट्या भागांची खरेदी करण्याबाबत अधिकार आहेत."

    return render(request, 'letter6.html', {
        'product': product,
        'grouped_subproducts': grouped_subproducts,
        'global_total_basic_price': global_total_basic_price,
        'quotations': quotations,
        'global_gst_value': global_gst_value,
        'global_total_price_inclusive': global_total_price_inclusive,
        'quotation_expense_criteria_text': quotation_expense_criteria_text,
    })

    
    
def product_list6(request):
    letters = Letter.objects.all()
    return render(request, 'table6.html', {'letters': letters})







def product_list7(request):
    letters = Letter.objects.all()
    return render(request, 'table7.html', {'letters': letters})


def letter_detail7(request, product_id):
    product = Product.objects.get(pk=product_id)
    subproducts = product.subproducts.all()
    letter = product.letter
    quotations = Quotation.objects.filter(product=product)

    grouped_subproducts = {}
    for subproduct in subproducts:
        provider_name = subproduct.amc_provider.name
        if provider_name not in grouped_subproducts:
            grouped_subproducts[provider_name] = []
        grouped_subproducts[provider_name].append(subproduct)

    return render(request, 'letter.html', {'product': product, 'grouped_subproducts': grouped_subproducts, 'letter': letter, 'quotations': quotations})


@csrf_exempt
def submit_form(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        letter_no = data.get('letter_no')
        lab_name = data.get('lab_name')
        letter_date = data.get('letter_date')

        letter = Letter.objects.create(
            letter_no=letter_no,
            lab_name=lab_name,
            letter_date=letter_date
        )

        products_data = data.get('products', [])
        for product_data in products_data:
            product = Product.objects.create(
                letter=letter,
                sr_no=product_data.get('Product SR'),
                name=product_data.get('Product Name'),
                price=product_data.get('Product Price'),
                buying_date=product_data.get('Buying Date'),
                department_name=product_data.get('Department Name')
            )

            subproducts_data = product_data.get('Subproducts', [])
            for subproduct_data in subproducts_data:
                amc_provider_name = subproduct_data.get('AMC Provider')
                amc_provider, created = AMCProvider.objects.get_or_create(name=amc_provider_name.strip())

                Subproduct.objects.create(
                    product=product,
                    type_of_part=subproduct_data.get('Type of Part'),
                    part_name=subproduct_data.get('Part Name'),
                    specification=subproduct_data.get('Specification'),
                    quantity=subproduct_data.get('Quantity'),
                    period_of_amc_contract=subproduct_data.get('Period of AMC Contract'),
                    service_report_date=subproduct_data.get('Service Report Date'),
                    amc_provider=amc_provider
                )

        return JsonResponse({'message': 'Form submitted successfully!'})

    return JsonResponse({'message': 'Error submitting form. Please try again.'}, status=400)



@csrf_exempt
def submit_quotation_info(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        date = request.POST.get('date')
        ref_no = request.POST.get('ref_no')
        quotation_expense_criteria = request.POST.get('quotation_criteria')

        # Create the quotation
        product = Product.objects.get(pk=product_id)
        quotation = Quotation.objects.create(
            product=product,
            quotation_date=date,
            ref_no=ref_no,
            quotation_expense_criteria=quotation_expense_criteria
        )

        total_price = 0  # Initialize total_price

        # Process each subproduct
        subproduct_ids = [key.split('_')[-1] for key in request.POST.keys() if key.startswith('subproduct_id')]
        for subproduct_id in subproduct_ids:
            subproduct = Subproduct.objects.get(pk=subproduct_id)
            amc_provider = subproduct.amc_provider

            unit_price = Decimal(request.POST.get(f'unit_price_{subproduct_id}'))  # Convert to Decimal
            quantity = subproduct.quantity
            price_without_gst = unit_price * quantity
            gst_value = price_without_gst * Decimal('0.18')  # Calculate GST value
            price_with_gst = price_without_gst + gst_value

            total_price += price_with_gst  # Add price_with_gst to total_price

            # Create the quotation item
            quotation_item = QuotationItem.objects.create(
                quotation=quotation,
                subproduct=subproduct,
                unit_price=unit_price,
                price_without_gst=price_without_gst,
                price_with_gst=price_with_gst,
                gst_percentage=18,  # Hardcoded GST percentage for now
                gst_value=gst_value,
                expected_delivery=request.POST.get(f'expected_delivery_{subproduct_id}'),
                amc_provider=amc_provider
            )

            # Update the AMCProvider fields (if needed)
            # Note: This part may need adjustment based on your actual requirements

        quotation.total_price = total_price  # Update total_price
        quotation.save()

        return JsonResponse({'message': 'Quotation information submitted successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
    