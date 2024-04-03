from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Letter, Product, Subproduct, Quotation, AMCProvider, QuotationItem
from itertools import groupby


def load_form(request):
    return render(request,'form1.html')


def product_list(request):
    letters = Letter.objects.all()
    return render(request, 'table.html', {'letters': letters})

def letter_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    subproducts = product.subproducts.all()
    return render(request, 'letter1.html', {'product': product,'subproducts':subproducts})

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
    amc_provider = subproduct.amc_provider
    related_subproducts = Subproduct.objects.filter(product=product, amc_provider=amc_provider)
    service_report_date = subproduct.service_report_date
    return render(request, 'letter4.html', {'product': product, 'amc_provider': amc_provider, 'related_subproducts': related_subproducts, 'service_report_date': service_report_date})





def letter_detail6(request, subproduct_id):
    subproduct = Subproduct.objects.get(pk=subproduct_id)
    product = subproduct.product
    amc_provider = subproduct.amc_provider
    subproducts = Subproduct.objects.filter(product=product).select_related('amc_provider')
    
    # Group subproducts by amc_provider name
    grouped_subproducts = {}
    for sub in subproducts:
        provider_name = sub.amc_provider.name
        if provider_name not in grouped_subproducts:
            grouped_subproducts[provider_name] = []
        grouped_subproducts[provider_name].append(sub)

    return render(request, 'letter6.html', {
        'product': product,
        'grouped_subproducts': grouped_subproducts,
    })



def product_list6(request):
    letters = Letter.objects.all()
    return render(request, 'table6.html', {'letters': letters})







def product_list7(request):
    letters = Letter.objects.filter(products__subproducts__quotationitem__isnull=False).distinct()
    
    return render(request, 'table7.html', {'letters': letters})


def letter_detail7(request, product_id):
    product = Product.objects.get(pk=product_id)
    subproducts = product.subproducts.all()
    letter = product.letter
    quotations = product.quotations.all()

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

        # Create the quotation
        product = Product.objects.get(pk=product_id)
        quotation = Quotation.objects.create(product=product, quotation_date=date, ref_no=ref_no)

        # Process each subproduct
        subproduct_ids = [key.split('_')[-1] for key in request.POST.keys() if key.startswith('subproduct_id_')]
        for subproduct_id in subproduct_ids:
            subproduct = Subproduct.objects.get(pk=subproduct_id)
            amc_provider = subproduct.amc_provider

            unit_price = request.POST.get(f'unit_price_{subproduct_id}')
            price_without_gst = request.POST.get(f'price_without_gst_{subproduct_id}')
            price_with_gst = request.POST.get(f'price_with_gst_{subproduct_id}')
            expected_delivery = request.POST.get(f'expected_delivery_{subproduct_id}')

            # Create the quotation item
            quotation_item = QuotationItem.objects.create(
                quotation=quotation,
                subproduct=subproduct,
                unit_price=unit_price,
                price_without_gst=price_without_gst,
                price_with_gst=price_with_gst,
                gst_percentage=((float(price_with_gst) - float(price_without_gst)) / float(price_without_gst)) * 100,
                gst_value=float(price_with_gst) - float(price_without_gst),
                expected_delivery=expected_delivery,
                amc_provider=amc_provider
            )

            # Update the AMCProvider fields
            amc_provider.ac_no = request.POST.get('ac_no', amc_provider.ac_no)
            amc_provider.ifsc_code = request.POST.get('ifsc_code', amc_provider.ifsc_code)
            amc_provider.ac_name = request.POST.get('ac_name', amc_provider.ac_name)
            amc_provider.bank_name = request.POST.get('bank_name', amc_provider.bank_name)
            amc_provider.pan_no = request.POST.get('pan_no', amc_provider.pan_no)
            amc_provider.state = request.POST.get('state', amc_provider.state)
            amc_provider.pincode = request.POST.get('pincode', amc_provider.pincode)
            amc_provider.address = request.POST.get('address', amc_provider.address)
            amc_provider.save()

        return JsonResponse({'message': 'Quotation information submitted successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
