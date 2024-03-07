from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Letter, Product, Subproduct, QuotationInfo, SubproductQuotationInfo, AMCProvider

# Create your views here.


def say_hello(request):
    return render(request,'index.html',{'name':'Samarth'})

def load_vendorInfo(request):
    return render(request,'vendor information.html')

def load_vendorId(request):
    return render(request,'vendor_identifier.html')

def load_vendorBankDetails(request):
    return render(request,'vendorBank.html')

def load_letter(request):
    return render(request,'letter.html')

def load_letter1(request):
    return render(request,'letter1.html')

def load_letter4(request):
    return render(request,'letter4.html')

    
def load_form(request):
    return render(request,'form1.html')

def load_demo(request):
    return render(request,'demo.html')

def product_list(request):
    letters = Letter.objects.all()
    return render(request, 'table.html', {'letters': letters})

def letter_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'letter1.html', {'product': product})

def quotation_form(request):
    letters = Letter.objects.all()
    return render(request, 'letter_intermidiate.html', {'letters': letters})

def quotation_page(request, product_id):
    product = Product.objects.get(pk=product_id)
    subproducts = product.subproducts.all()
    return render(request, 'quotation_info.html', {'product': product, 'subproducts': subproducts})



def product_list4(request):
    letters = Letter.objects.all()
    return render(request, 'table2.html', {'letters': letters})


def letter_detail4(request, subproduct_id):
    subproduct = Subproduct.objects.get(pk=subproduct_id)
    product = subproduct.product
    amc_provider = subproduct.amc_provider
    related_subproducts = Subproduct.objects.filter(product=product, amc_provider=amc_provider)
    service_report_date = subproduct.service_report_date  # Assuming service_report_date is a field of Subproduct
    return render(request, 'letter4.html', {'product': product, 'amc_provider': amc_provider, 'related_subproducts': related_subproducts, 'service_report_date': service_report_date})

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
                Subproduct.objects.create(
                    product=product,
                    type_of_part=subproduct_data.get('Type of Part'),
                    part_name=subproduct_data.get('Part Name'),
                    specification=subproduct_data.get('Specification'),
                    quantity=subproduct_data.get('Quantity'),
                    period_of_amc_contract=subproduct_data.get('Period of AMC Contract'),
                    service_report_date=subproduct_data.get('Service Report Date'),
                    amc_provider=subproduct_data.get('AMC Provider')
                )

        return JsonResponse({'message': 'Form submitted successfully!'})

    return JsonResponse({'message': 'Error submitting form. Please try again.'}, status=400)




def submit_quotation_info(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        date = request.POST.get('date')
        ref_no = request.POST.get('ref_no')

        quotation_info = QuotationInfo(product_id=product_id, date=date, ref_no=ref_no)
        quotation_info.save()

        for subproduct in request.POST:
            if subproduct.startswith('price_without_gst_'):
                subproduct_id = subproduct.split('_')[-1]
                price_without_gst = request.POST.get(subproduct)
                price_with_gst = request.POST.get('price_with_gst_' + subproduct_id)
                expected_delivery = request.POST.get('expected_delivery_' + subproduct_id)
                amc_provider_name = request.POST.get('amc_provider_name_' + subproduct_id)
                ac_no = request.POST.get('ac_no_' + subproduct_id)
                ifsc_code = request.POST.get('ifsc_code_' + subproduct_id)
                ac_name = request.POST.get('ac_name_' + subproduct_id)
                bank_name = request.POST.get('bank_name_' + subproduct_id)
                pan_no = request.POST.get('pan_no_' + subproduct_id)

                if amc_provider_name:
                    amc_provider, created = AMCProvider.objects.get_or_create(
                        name=amc_provider_name,
                        ac_no=ac_no,
                        ifsc_code=ifsc_code,
                        ac_name=ac_name,
                        bank_name=bank_name,
                        pan_no=pan_no
                    )
                else:
                    return JsonResponse({'message': 'AMC Provider name cannot be empty'}, status=400)

                subproduct_quotation_info = SubproductQuotationInfo(
                    quotation_info_id=quotation_info.id,
                    subproduct_id=subproduct_id,
                    price_without_gst=price_without_gst,
                    price_with_gst=price_with_gst,
                    expected_delivery=expected_delivery,
                    amc_provider=amc_provider
                )
                subproduct_quotation_info.save()

        return JsonResponse({'message': 'Quotation information submitted successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
