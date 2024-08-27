from decimal import Decimal
from django.db.models import Exists, OuterRef,Q
from collections import defaultdict
from django.http import Http404
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.db.models import Prefetch 
import datetime
from .models import Letter, Product, Subproduct, Quotation, AMCProvider, QuotationItem,MainItem,Manufacturer,Department,Lab,PrintTrack,ServiceReportTrack
from django.db.models import Count
from .forms import ItemForm, ManufacturerForm
from django.shortcuts import render, redirect
from .forms import MainItemForm
from django.contrib import messages
from .forms import ProductForm
from django.core.serializers.json import DjangoJSONEncoder
from .forms import AMCProviderForm
from django.urls import reverse
from django.db import transaction


#mainitems
def items_list(request):
    items = MainItem.objects.all()
    return render(request, 'items.html', {'mitem': items})

def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item added successfully.')
            return redirect('items_list')
    else:
        form = ItemForm()

    manufacturers = Manufacturer.objects.all()
    return render(request, 'add_item.html', {'form': form, 'manufacturers': manufacturers})

def edit_item(request, item_id):
    item = get_object_or_404(MainItem, pk=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully.')
            return redirect('items_list')
    else:
        form = ItemForm(instance=item)

    manufacturers = Manufacturer.objects.all()
    return render(request, 'edit_item.html', {'form': form, 'item': item, 'manufacturers': manufacturers})

def delete_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')
        item = get_object_or_404(MainItem, pk=item_id)
        item.delete()
        messages.success(request, 'Item deleted successfully.')
    return redirect('items_list')
# def product_list1(request):
#     products = Product.objects.all()
#     return render(request, 'items.html', {'products': products})


#manufacturer
def manufacturer_list(request):
    manufacturers = Manufacturer.objects.all()
    return render(request, 'manufacturer.html', {'manufacturers': manufacturers})


def edit_manufacturer(request, manufacturer_id):
    manufacturer = Manufacturer.objects.get(id=manufacturer_id)
    if request.method == 'POST':
        form = ManufacturerForm(request.POST, instance=manufacturer)
        if form.is_valid():
            form.save()
            return redirect('manufacturer_list')
    else:
        form = ManufacturerForm(instance=manufacturer)
    return render(request, 'edit_manufacturer.html', {'form': form})


def delete_manufacturer(request):
    if request.method == 'POST':
        manufacturer_id = request.POST.get('id')
        manufacturer = get_object_or_404(Manufacturer, id=manufacturer_id)
        manufacturer.delete()
        messages.success(request, 'Manufacturer deleted successfully!')
    return redirect('manufacturer_list')

def add_manufacturer(request):
    if request.method == 'POST':
        form = ManufacturerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manufacturer_list')  # Assuming you have a URL named 'manufacturer_list'
    else:
        form = ManufacturerForm()
    return render(request, 'add_manufacturer.html', {'form': form})

def add_product_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list_view')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


def manufacturer_list(request):
    return render(request,'manufacturer_list.html')  

def mitem(request):
    mitem = MainItem.objects.all()
    context = {'mitem':mitem}
    return render(request, 'items.html', context)

def manufacturer_view(request):
    manufacturers = Manufacturer.objects.all()
    context = {'manufacturers': manufacturers}  
    return render(request, 'manufacturer.html', context)
    
def index(request):
    return render(request,'index.html')

def items(request):
    return render(request,'items.html')

def manufacturer(request):
    return render(request,'manufacturer.html')

def track_letter(request, letter_id):
    try:
        letter = get_object_or_404(Letter, id=letter_id)
        print_track = get_object_or_404(PrintTrack, letter_no=letter.letter_no)
    except Http404:
        return render(request, 'print_error.html')
    return render(request, 'tracking.html', {'letter': letter, 'print_track': print_track})



def tracking_table(request):
    letters = Letter.objects.select_related('lab_name').prefetch_related(
        Prefetch('subproducts', queryset=Subproduct.objects.select_related('product__main_item', 'product__department'))
    ).all()

    context = {
        'letters': letters
    }

    return render(request, 'tracking_table.html', context)
 
def manufacturer_list(request):
    manufacturers = Manufacturer.objects.all()
    return render(request, 'manufacturer_list.html', {'manufacturers': manufacturers})

@csrf_exempt
def add_amc_provider(request):
    if request.method == 'POST':
        # Process form data
        name = request.POST.get('name')
        ac_no = request.POST.get('ac_no')
        ifsc_code = request.POST.get('ifsc_code')
        ac_name = request.POST.get('ac_name')
        bank_name = request.POST.get('bank_name')
        pan_no = request.POST.get('pan_no')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        address = request.POST.get('address')
        email_id = request.POST.get('email_id')
        contact_no = request.POST.get('contact_no')

        # Validate and save data
        try:
            provider = AMCProvider.objects.create(
                name=name,
                ac_no=ac_no,
                ifsc_code=ifsc_code,
                ac_name=ac_name,
                bank_name=bank_name,
                pan_no=pan_no,
                state=state,
                pincode=pincode,
                address=address,
                email_id=email_id,
                contact_no=contact_no
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def amc_providers_list(request):
    providers = AMCProvider.objects.all()
    serialized_providers = json.dumps(list(providers.values()), cls=DjangoJSONEncoder)
    return render(request, 'amc_providers_list.html', {'providers': providers, 'serialized_providers': serialized_providers})

def edit_amc_provider(request, id):
    provider = get_object_or_404(AMCProvider, pk=id)
    if request.method == 'POST':
        form = AMCProviderForm(request.POST, instance=provider)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('amc_providers_list'))  # Redirect to the AMC Providers list
    else:
        form = AMCProviderForm(instance=provider)
    
    return render(request, 'edit_amc_provider.html', {'form': form, 'provider': provider})
def confirm_delete_amc_provider(request, id):
    provider = get_object_or_404(AMCProvider, id=id)
    return render(request, 'confirm_delete_amc.html', {'provider': provider})

def delete_amc_provider(request, id):
    provider = get_object_or_404(AMCProvider, id=id)
    provider.delete()
    return redirect('amc_providers_list')

def get_sr_numbers(request):
    lab_id = request.GET.get('lab_id')
    main_item = request.GET.get('main_item')
    manufacturer = request.GET.get('manufacturer')
    department_id = request.GET.get('department_id')

    # Ensure all parameters are provided
    if lab_id and main_item and manufacturer and department_id:
        sr_numbers = Product.objects.filter(
            lab_name__id=lab_id,
            main_item__name=main_item,
            main_item__manufacturer__name=manufacturer,
            department__id=department_id  # Assuming the correct field name in the model
        ).values_list('sr_no', flat=True).distinct()
        
        sr_numbers_list = list(sr_numbers)
        return JsonResponse({'sr_numbers': sr_numbers_list})
    
    # If any parameter is missing, return an empty list with an appropriate message
    return JsonResponse({'sr_numbers': [], 'message': 'Missing parameters'}, status=400)


def load_form(request):
    # Fetch required context data for the form
    main_items = MainItem.objects.values('name', 'id').annotate(total=Count('name')).filter(total=1)
    labs = Lab.objects.all()
    manufacturer_names = list(Manufacturer.objects.values_list('name', flat=True))
    departments = Department.objects.all()
    
    # Fetch all letters with their related products and subproducts for the product information table
    letters = Letter.objects.prefetch_related('products__subproducts').all()

    context = {
        'main_items': main_items,
        'manufacturer_names': manufacturer_names,
        'departments': departments,
        'labs': labs,
        'letters': letters
    }

    return render(request, 'form1.html', context)


def update_print_date(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        letter_no = data.get('letter_no')
        letter_field = data.get('letter_field')  # New field to indicate which letter's print date to update
        
        try:
            print_track, created = PrintTrack.objects.get_or_create(letter_no=letter_no)
            
            # Update the specific letter's print date based on the field sent from the frontend
            if letter_field == 'letter1' and not print_track.printed_date1:
                print_track.printed_date1 = timezone.now()
            elif letter_field == 'letter2' and not print_track.printed_date2:
                print_track.printed_date2 = timezone.now()
            elif letter_field == 'letter3' and not print_track.printed_date3:
                print_track.printed_date3 = timezone.now()
            elif letter_field == 'letter4' and not print_track.printed_date4:
                print_track.printed_date4 = timezone.now()

            print_track.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def get_manufacturers(request):
    main_item = request.GET.get('main_item')
    print(f"Received main_item: {main_item}")  # Debugging statement
    if main_item:
        manufacturers = Manufacturer.objects.filter(mainitem__name=main_item).values_list('name', flat=True).distinct()
    else:
        manufacturers = Manufacturer.objects.none()
    print(f"Manufacturers found: {list(manufacturers)}")  # Debugging statement
    return JsonResponse({'manufacturer_names': list(manufacturers)})



def get_manufacturer_names(request):
    main_item = request.GET.get('main_item')
    manufacturers = Manufacturer.objects.filter(mainitem__name=main_item).values_list('name', flat=True).distinct()
    return JsonResponse({'manufacturer_names': list(manufacturers)})
def get_product_serial_numbers(request):
    lab_id = request.GET.get('lab_id')
    main_item = request.GET.get('main_item')
    manufacturer = request.GET.get('manufacturer')
    department_id = request.GET.get('department_id')

    products = Product.objects.filter(lab_id=lab_id, main_item=main_item, manufacturer__name=manufacturer, department_id=department_id).values_list('serial_number', flat=True)
    
    return JsonResponse({'product_serial_numbers': list(products)})
# Product list view
def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def get_product_serial_numbers(request):
    lab_id = request.GET.get('lab_id')
    main_item = request.GET.get('main_item')
    manufacturer = request.GET.get('manufacturer')
    department_id = request.GET.get('department_id')

    products = Product.objects.filter(lab_id=lab_id, main_item=main_item, manufacturer__name=manufacturer, department_id=department_id).values_list('serial_number', flat=True)
    
    return JsonResponse({'product_serial_numbers': list(products)})

def get_departments(request):
    lab_id = request.GET.get('lab_id')
    departments = Department.objects.filter(lab_id=lab_id).values('id', 'name')
    return JsonResponse({'departments': list(departments)})

# Edit product view
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            # Add a success message if needed
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list_view')  # Redirect to product_list URL name
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'edit_product.html', {'form': form})


# Delete product view
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product_list_view')
    return render(request, 'product_list.html')

def product_detail_json(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        data = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'buying_date': product.buying_date,
            'department': product.department.name,
            'lab_name': product.lab_name.name,
            'amc_provider': product.amc_provider.name,
            'amc_period': product.amc_period,
            'expenditure_cost': product.expenditure_cost,
            'manufacturer_warranty_period': product.manufacturer_warranty_period,
            'service_report_date': product.service_report_date,
            'manufacturer': product.manufacturer
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    #am-provider
def amc_providers_list(request):
    providers = AMCProvider.objects.all()
    return render(request, 'amc_providers_list.html', {'providers': providers})


#service report history
def service_report_history(request):
    products = Product.objects.all()
    return render(request, 'service_report_history.html', {'products': products})

def product_list(request):
    # Retrieve all Letter objects with required fields
    letters = Letter.objects.select_related('lab_name').prefetch_related('subproducts__product__main_item', 'subproducts__product__department').all()

    # Get letter numbers where is_done is True
    done_letters = PrintTrack.objects.filter(is_done=True).values_list('letter_no', flat=True)

    # Exclude letters with letter_no in done_letters
    letters = letters.exclude(letter_no__in=done_letters)

    # Pass the data to the template
    context = {
        'letters': letters
    }

    # Render the template with the provided context
    return render(request, 'table.html', context)

def letter_detail(request, letter_id):
    # Fetch the letter
    letter = get_object_or_404(Letter, id=letter_id)
    
    # Get the AMC provider ID from the query parameters
    amc_provider_id = request.GET.get('amc_provider_id')
    
    # Get all subproducts associated with the letter
    subproducts = Subproduct.objects.filter(letters=letter).distinct()
    
    # Filter subproducts by the specific AMC provider if provided
    if amc_provider_id:
        amc_provider = get_object_or_404(AMCProvider, id=amc_provider_id)
        subproducts = subproducts.filter(amc_provider=amc_provider)
    else:
        amc_provider = None
    
    # Group subproducts by amc_provider
    grouped_subproducts = defaultdict(list)
    for subproduct in subproducts:
        grouped_subproducts[subproduct.amc_provider].append(subproduct)
    
    # Get the product associated with the first subproduct (assuming all subproducts have the same product)
    product = subproducts.first().product if subproducts.exists() else None

    # Accessing service report date from the product's service reports
    service_report_date = product.service_reports.latest('service_date').service_date if product and product.service_reports.exists() else None

    # Collect the product serial number
    product_serial_number = str(product.sr_no) if product else ''

    # Get the current date
    current_date = timezone.now()

    return render(request, 'letter1.html', {
        'product': product,
        'amc_provider': amc_provider,
        'letters': [letter],  # Wrap the single letter in a list to maintain template structure
        'subproducts': subproducts,
        'grouped_subproducts': grouped_subproducts,
        'current_date': current_date,
        'service_report_date': service_report_date,
        'product_serial_number': product_serial_number
    })


def quotation_form(request):
    # Retrieve all Letter objects with required fields
    letters = Letter.objects.select_related('lab_name').prefetch_related('subproducts__product__main_item', 'subproducts__product__department').all()

    # Get letter numbers where is_done is True
    done_letters = PrintTrack.objects.filter(is_done=True).values_list('letter_no', flat=True)

    # Exclude letters with letter_no in done_letters
    letters = letters.exclude(letter_no__in=done_letters)

    # Filter letters where Quotation does not exist
    letters_without_quotation = []
    for letter in letters:
        if not Quotation.objects.filter(letter=letter).exists():
            letters_without_quotation.append(letter)

    # Pass the data to the template
    context = {
        'letters': letters_without_quotation
    }

    # Render the template with the provided context
    return render(request, 'letter_intermidiate.html', context)


def quotation_page(request, letter_id):
    # Fetch the letter
    letter = get_object_or_404(Letter, pk=letter_id)

    # Get the AMC provider ID from the query parameters
    amc_provider_id = request.GET.get('amc_provider_id')

    # Filter subproducts based on AMCProvider if amc_provider_id is provided
    if amc_provider_id:
        amc_provider = get_object_or_404(AMCProvider, pk=amc_provider_id)
        subproducts = letter.subproducts.filter(amc_provider=amc_provider)
    else:
        subproducts = letter.subproducts.all()

    # Filter products associated with the filtered subproducts
    products = Product.objects.filter(subproducts__in=subproducts).distinct()

    # Get existing AMC providers
    amc_providers_exist = set(AMCProvider.objects.values_list('name', flat=True))

    return render(request, 'quotation_info.html', {
        'letter': letter,
        'products': products,
        'subproducts': subproducts,
        'amc_providers_exist': amc_providers_exist,
        'amc_provider_id': amc_provider_id  # Pass amc_provider_id to template if needed
    })



def product_list4(request):
    # Retrieve all Letter objects with required fields
    letters = Letter.objects.select_related('lab_name').prefetch_related('subproducts__product__main_item', 'subproducts__product__department').all()

    # Get letter numbers where is_done is True
    done_letters = PrintTrack.objects.filter(is_done=True).values_list('letter_no', flat=True)

    # Exclude letters with letter_no in done_letters
    letters = letters.exclude(letter_no__in=done_letters)

    # Pass the data to the template
    context = {
        'letters': letters
    }

    # Render the template with the provided context
    return render(request, 'table2.html', context)
    


def letter_detail4(request, letter_id):
    # Fetch the letter
    letter = get_object_or_404(Letter, id=letter_id)
    subproducts = letter.subproducts.all()

    # Get the AMC provider ID from the query parameters
    amc_provider_id = request.GET.get('amc_provider_id')

    # Get the specific AMC provider and filter subproducts
    if amc_provider_id:
        amc_provider = get_object_or_404(AMCProvider, id=amc_provider_id)
        related_subproducts = subproducts.filter(amc_provider=amc_provider)
    else:
        amc_provider = None
        related_subproducts = subproducts

    # Get the products associated with the subproducts
    products = related_subproducts.values_list('product', flat=True).distinct()
    products = Product.objects.filter(id__in=products)

    # Accessing service report dates for all products
    service_report_dates = {}
    for product in products:
        if product.service_reports.exists():
            service_report_dates[product.id] = product.service_reports.latest('service_date').service_date
        else:
            service_report_dates[product.id] = None

    # Collect the product serial numbers
    product_serial_numbers = {product.id: str(product.sr_no) for product in products}

    return render(request, 'letter4.html', {
        'products': products,
        'amc_provider': amc_provider,
        'related_subproducts': related_subproducts,
        'service_report_dates': service_report_dates,
        'letter': letter,
        'product_serial_numbers': product_serial_numbers
    })




def letter_detail6(request, letter_id):
    # Fetch the letter object or return a 404 if not found
    letter = get_object_or_404(Letter, pk=letter_id)
    
    # Fetch subproducts related to the letter and their related amc_provider and product
    subproducts = letter.subproducts.select_related('amc_provider', 'product')
    product = subproducts.first().product if subproducts else None
    main_item = product.main_item if product else None

    # Ensure all quotations related to the letter are fetched
    quotations = Quotation.objects.filter(letter=letter).distinct()

    # Initialize global variables
    global_total_basic_price = Decimal('0')
    global_gst_value = Decimal('0')
    global_total_price_inclusive = Decimal('0')

    current_date = timezone.now()

    # Group subproducts by AMC provider name
    grouped_subproducts = {}
    unique_amc_providers = set()
    for sub in subproducts:
        provider_name = sub.amc_provider.name if sub.amc_provider else 'Unknown'
        if provider_name not in grouped_subproducts:
            grouped_subproducts[provider_name] = []
        grouped_subproducts[provider_name].append(sub)

        # Collect unique AMC providers by name
        unique_amc_providers.add(provider_name)

        # Fetch the related QuotationItem and compute costs
        quotation_item = QuotationItem.objects.filter(subproduct=sub).first()
        if quotation_item:
            total_basic_price = quotation_item.unit_price * sub.quantity
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
            quotation_expense_criteria_text = (
                "शासन निर्णय, वित्त विभाग, क्रमांकः विअप्र-२०१३/प्र.क.३०/२०१३/विनियम, दिनांक १७ एप्रिल , २०१५ "
                "अन्वये भाग पहिला उपविभाग. २ अनुक्रमांक. ५ नियम क्र.७ यंत्राच्या कार्यसज्जतेसाठी लागणारे सुटे "
                "भाग, उपसाधने व इतर वस्तू साधनसामग्री विकत घेण्यासाठी मंजूरी देणे करिता यंत्र सामग्रीच्या पुस्तकी "
                "किमतीच्या २०% मर्यादेपर्यंत विभाग प्रमुख व प्रादेशिक कार्यालय प्रमुख यांना दरपत्रक मागून सुट्ट्या "
                "भागांची खरेदी करण्याबाबत अधिकार आहेत."
            )
        elif quotation.quotation_expense_criteria == '25%':
            quotation_expense_criteria_text = (
                "शासन निर्णय, वित्त विभाग, क्रमांकः विअप्र-२०१३/प्र.क.३०/२०१३/विनियम, दिनांक १७ एप्रिल , २०१५ "
                "अन्वये भाग पहिला उपविभाग. २ अनुक्रमांक. ५ नियम क्र.७ यंत्राच्या कार्यसज्जतेसाठी लागणारे सुटे "
                "भाग, उपसाधने व इतर वस्तू साधनसामग्री विकत घेण्यासाठी मंजूरी देणेसंयत्रे , यंत्रसामग्री आणि "
                "साधनसामग्री इत्यादीच्या दुरुस्ती करिता वार्षिक खर्च यंत्रसामग्रीच्या पुस्तकी किंमतीच्या 25% "
                "मर्यादेपर्यंत विभाग प्रमुख व प्रादेशिक कार्यालय प्रमुख यांना दरपत्रक मागून सुट्ट्या भागांची खरेदी "
                "करण्याबाबत अधिकार आहेत."
            )

    # Fetch PrintTrack instance related to the letter
    print_track = get_object_or_404(PrintTrack, letter_no=letter.letter_no)

    return render(request, 'letter6.html', {
        'letter': letter,
        'main_item': main_item,  # Pass main_item to the template
        'product': product,
        'current_date': current_date,  # Corrected variable name
        'grouped_subproducts': grouped_subproducts,
        'global_total_basic_price': global_total_basic_price,
        'quotations': quotations,
        'global_gst_value': global_gst_value,
        'global_total_price_inclusive': global_total_price_inclusive,
        'quotation_expense_criteria_text': quotation_expense_criteria_text,
        'unique_amc_providers': unique_amc_providers,  # Pass the list of unique AMC provider names
        'print_track': print_track,  # Pass PrintTrack instance to the template
    })


    
def product_list6(request):
    # Retrieve all Letter objects with required fields
    letters = Letter.objects.select_related('lab_name').prefetch_related(
        'subproducts__product__main_item', 'subproducts__product__department'
    ).all()

    # Get letter numbers where is_done is True
    done_letters = PrintTrack.objects.filter(is_done=True).values_list('letter_no', flat=True)

    # Exclude letters with letter_no in done_letters
    letters = letters.exclude(letter_no__in=done_letters)

    # Filter letters where Quotation exists
    letters_with_quotation = letters.filter(quotation__isnull=False).distinct()

    # Pass the data to the template
    context = {
        'letters': letters_with_quotation
    }

    # Render the template with the provided context
    return render(request, 'table6.html', context)    







def product_list7(request):
        # Retrieve all Letter objects with required fields
    letters = Letter.objects.select_related('lab_name').prefetch_related(
        'subproducts__product__main_item', 'subproducts__product__department'
    ).all()

    # Get letter numbers where is_done is True
    done_letters = PrintTrack.objects.filter(is_done=True).values_list('letter_no', flat=True)

    # Exclude letters with letter_no in done_letters
    letters = letters.exclude(letter_no__in=done_letters)

    # Filter letters where Quotation exists
    letters_with_quotation = letters.filter(quotation__isnull=False).distinct()

    # Pass the data to the template
    context = {
        'letters': letters_with_quotation
    }

    # Render the template with the provided context
    return render(request, 'table7.html', context)       



def letter_detail7(request, letter_id):
    # Fetch the letter using letter_id
    letter = get_object_or_404(Letter, pk=letter_id)

    # Get all subproducts associated with the letter
    subproducts = letter.subproducts.all()

    # Initialize containers for quotations
    quotations = set()

    # Fetch all quotations related to the subproducts
    for subproduct in subproducts:
        # Fetch quotation items related to the current subproduct
        quotation_items = QuotationItem.objects.filter(subproduct=subproduct)

        # Fetch quotations related to these quotation items and add to set
        for quotation_item in quotation_items:
            quotations.add(quotation_item.quotation)

    # Convert the set of quotations to a list (if needed)
    quotations = list(quotations)  # Assuming there's only one unique quotation

    # Initialize grouped subproducts dictionary
    grouped_subproducts = {}

    # Get the AMC provider ID from the query parameters
    amc_provider_id = request.GET.get('amc_provider_id')

    # Filter subproducts by the specified AMC provider if provided
    if amc_provider_id:
        amc_provider = get_object_or_404(AMCProvider, id=amc_provider_id)
        subproducts = subproducts.filter(amc_provider=amc_provider)

    # Group the subproducts by their AMC providers and collect necessary information
    for subproduct in subproducts:
        provider = subproduct.amc_provider
        provider_name = provider.name
        if provider_name not in grouped_subproducts:
            grouped_subproducts[provider_name] = {
                'address': provider.address,
                'state': provider.state,
                'pincode': provider.pincode,
                'email_id': provider.email_id,
                'contact_no': provider.contact_no,
                'types_of_part': set(),
                'products': set(),
                'parts_and_dates': {},
                'subproducts': []
            }
        grouped_subproducts[provider_name]['types_of_part'].add(subproduct.type_of_part)
        grouped_subproducts[provider_name]['products'].add((subproduct.product.main_item.name, subproduct.product.sr_no))
        
        # Group parts and dates by service date
        service_date = subproduct.product.service_report_date
        if service_date:
            if service_date not in grouped_subproducts[provider_name]['parts_and_dates']:
                grouped_subproducts[provider_name]['parts_and_dates'][service_date] = []
            grouped_subproducts[provider_name]['parts_and_dates'][service_date].append(subproduct.part_name)
        
        grouped_subproducts[provider_name]['subproducts'].append(subproduct)

    print_track = PrintTrack.objects.filter(letter_no=letter.letter_no).first()

    # Convert sets to lists for easier template rendering
    for provider in grouped_subproducts.values():
        provider['types_of_part'] = ', '.join(provider['types_of_part'])
        provider['products'] = ', '.join([f"{name} (Sr. No. {sr_no})" for name, sr_no in provider['products']])
        
        # Format parts and dates, ensuring each date is only listed once
        provider['parts_and_dates'] = ', '.join(
            [f"{date} - {', '.join(parts)}" for date, parts in provider['parts_and_dates'].items()]
        )

    return render(request, 'letter.html', {
        'letter': letter,
        'grouped_subproducts': grouped_subproducts,
        'quotation': quotations[0] if quotations else None,
        'amc_provider_id': amc_provider_id,
        'print_track': print_track  # Include PrintTrack object in the context

    })


def get_service_report_dates(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        current_service_date = product.service_report_date.strftime('%Y-%m-%d') if product.service_report_date else 'Not available'
        
        # Fetch earlier service date from ServiceReportTrack model
        earlier_service_date_obj = ServiceReportTrack.objects.filter(product=product).order_by('-service_date').first()
        earlier_service_date = earlier_service_date_obj.service_date.strftime('%Y-%m-%d') if earlier_service_date_obj else 'Not available'
        
        data = {
            'current_service_date': current_service_date,
            'earlier_service_date': earlier_service_date,
        }
        
        return JsonResponse(data)
    
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)


@csrf_exempt
@transaction.atomic  # Ensures that the database remains consistent
def submit_form(request):
    if request.method == 'POST':
        try:
            # Get form data
            letter_no = request.POST.get('letter_no')
            lab_name_id = request.POST.get('lab_name')
            letter_date = request.POST.get('date')

            if not lab_name_id.isdigit():
                raise ValueError(f"lab_name_id is not a digit: {lab_name_id}")

            # Validate and parse the letter date
            try:
                letter_date = datetime.datetime.strptime(letter_date, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError(f"Letter date {letter_date} is not in the correct format YYYY-MM-DD")

            # Create a Letter instance
            letter = Letter.objects.create(
                letter_no=letter_no,
                lab_name_id=lab_name_id,
                letter_date=letter_date
            )

            # Process products and subproducts
            product_index = 0
            while True:
                sr_no = request.POST.get(f'products[{product_index}][sr_no]')
                service_report_date = request.POST.get(f'products[{product_index}][service_report_date]')

                if not sr_no:
                    break

                # Find the product by SR No
                try:
                    product = Product.objects.get(sr_no=sr_no)
                    amc_provider = product.amc_provider  # Use AMC provider from Product model
                except Product.DoesNotExist:
                    raise ValueError(f"Product with SR No {sr_no} does not exist")

                # Validate and update the service report date if provided
                if service_report_date:
                    try:
                        service_report_date = datetime.datetime.strptime(service_report_date, '%Y-%m-%d').date()
                    except ValueError:
                        raise ValueError(f"Service report date {service_report_date} is not in the correct format YYYY-MM-DD")

                    # Update service report date and track changes
                    if product.service_report_date != service_report_date:
                        ServiceReportTrack.objects.create(product=product, service_date=product.service_report_date)
                        product.service_report_date = service_report_date
                        product.save()

                # Process subproducts
                subproduct_index = 0
                while True:
                    part_name = request.POST.get(f'products[{product_index}][subproducts][{subproduct_index}][part_name]')
                    if not part_name:
                        break

                    part_type = request.POST.get(f'products[{product_index}][subproducts][{subproduct_index}][part_type]')
                    part_specification = request.POST.get(f'products[{product_index}][subproducts][{subproduct_index}][part_specification]')
                    part_quantity = request.POST.get(f'products[{product_index}][subproducts][{subproduct_index}][part_quantity]')
                    unit_of_measure = request.POST.get(f'products[{product_index}][subproducts][{subproduct_index}][unit_of_measurement]')

                    if not part_quantity.isdigit():
                        raise ValueError(f"Part quantity is not a digit: {part_quantity}")

                    # Create a Subproduct instance
                    subproduct = Subproduct.objects.create(
                        product=product,
                        part_name=part_name,
                        type_of_part=part_type,
                        specification=part_specification,
                        quantity=int(part_quantity),
                        unit_of_measure=unit_of_measure,
                        amc_provider=amc_provider  # Link AMC provider from the Product model
                    )

                    # Link subproduct to the letter
                    letter.subproducts.add(subproduct)

                    subproduct_index += 1

                product_index += 1

            # If everything is successful, commit the transaction and return success
            return JsonResponse({'success': True})

        except Exception as e:
            # If an error occurs, return the error as a JSON response
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


def submit_quotation_info(request):
    if request.method == 'POST':
        letter_id = request.POST.get('letter_id')
        date = request.POST.get('date')
        ref_no = request.POST.get('ref_no')
        quotation_expense_criteria = request.POST.get('quotation_criteria')

        letter = get_object_or_404(Letter, pk=letter_id)

        subproduct_ids = [key.split('_')[-1] for key in request.POST.keys() if key.startswith('subproduct_id')]
        for subproduct_id in subproduct_ids:
            subproduct = get_object_or_404(Subproduct, pk=subproduct_id)

            unit_price = Decimal(request.POST.get(f'unit_price_{subproduct_id}', '0'))
            quantity = subproduct.quantity
            price_without_gst = unit_price * quantity
            gst_value = price_without_gst * Decimal('0.18')
            price_with_gst = price_without_gst + gst_value

            total_price = price_with_gst

            # Create a new Quotation for the Letter and ref_no
            quotation = Quotation.objects.create(
                letter=letter,
                ref_no=ref_no,
                quotation_date=date,
                quotation_expense_criteria=quotation_expense_criteria,
                total_price=0  # Initialize with 0, will be updated later
            )

            # Create the QuotationItem associated with the Quotation
            QuotationItem.objects.create(
                quotation=quotation,
                subproduct=subproduct,
                unit_price=unit_price,
                price_without_gst=price_without_gst,
                price_with_gst=price_with_gst,
                gst_percentage=18,
                gst_value=gst_value,
                expected_delivery=request.POST.get(f'expected_delivery_{subproduct_id}'),
                amc_provider=subproduct.amc_provider
            )

            # Update the total price of the quotation
            quotation.total_price += total_price
            quotation.save()

        return JsonResponse({'message': 'Quotation information submitted successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)


@csrf_exempt
def add_amc_provider(request):
    if request.method == 'POST':
        provider = AMCProvider(
            name=request.POST['name'],
            ac_no=request.POST['ac_no'],
            ifsc_code=request.POST['ifsc_code'],
            ac_name=request.POST['ac_name'],
            bank_name=request.POST['bank_name'],
            pan_no=request.POST['pan_no'],
            state=request.POST['state'],
            pincode=request.POST['pincode'],
            address=request.POST['address'],
            email_id=request.POST['email_id'],
            contact_no=request.POST['contact_no']
        )
        provider.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})