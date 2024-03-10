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


def letter_detail6(request, subproduct_id):
    subproduct = Subproduct.objects.get(pk=subproduct_id)
    product = subproduct.product
    amc_provider = subproduct.amc_provider
    subproductquotationinfo = SubproductQuotationInfo.objects.get(subproduct=subproduct)
    letter = product.letter  # Assuming there is a ForeignKey from Product to Letter

    return render(request, 'letter6.html', {'product': product, 'subproduct': subproduct, 'amc_provider': amc_provider, 'subproductquotationinfo': subproductquotationinfo, 'letter': letter})

def product_list6(request):
    letters = Letter.objects.all()
    return render(request, 'table6 .html', {'letters': letters})

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



@csrf_exempt
def submit_quotation_info(request):
    if request.method == 'POST':
        subproduct_id = request.POST.get('subproduct_id')
        date = request.POST.get('date')
        ref_no = request.POST.get('ref_no')

        quotation_info = QuotationInfo.objects.create(subproduct_id=subproduct_id, date=date, ref_no=ref_no)

        unit_price = request.POST.get('unit_price')
        price_without_gst = request.POST.get('price_without_gst')
        price_with_gst = request.POST.get('price_with_gst')
        expected_delivery = request.POST.get('expected_delivery')

        amc_provider_name = request.POST.get('amc_provider_name')
        ac_no = request.POST.get('ac_no')
        ifsc_code = request.POST.get('ifsc_code')
        ac_name = request.POST.get('ac_name')
        bank_name = request.POST.get('bank_name')
        pan_no = request.POST.get('pan_no')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        address = request.POST.get('address')

        amc_provider, created = AMCProvider.objects.get_or_create(
            name=amc_provider_name,
            ac_no=ac_no,
            ifsc_code=ifsc_code,
            ac_name=ac_name,
            bank_name=bank_name,
            pan_no=pan_no,
            state=state,
            pincode=pincode,
            address=address
        )

        subproduct_quotation_info = SubproductQuotationInfo.objects.create(
            quotation_info=quotation_info,
            subproduct_id=subproduct_id,
            unit_price=unit_price,
            price_without_gst=price_without_gst,
            price_with_gst=price_with_gst,
            gst_percentage=((float(price_with_gst) - float(price_without_gst)) / float(price_without_gst)) * 100,
            gst_value=float(price_with_gst) - float(price_without_gst),
            expected_delivery=expected_delivery,
            amc_provider=amc_provider
        )

        return JsonResponse({'message': 'Quotation information submitted successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)