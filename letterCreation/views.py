from decimal import Decimal
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from django.http import HttpResponseRedirect

import datetime
from .models import Letter, Product, Subproduct, Quotation, AMCProvider, QuotationItem,MainItem,Manufacturer,Department,Lab
from django.db.models import Count
from .forms import ManufacturerForm
from django.shortcuts import render, redirect
from .forms import MainItemForm
from django.contrib import messages
from .forms import ProductForm
from django.core.serializers.json import DjangoJSONEncoder
from .forms import AMCProviderForm
from django.urls import reverse


def try1(request):
    return render(request,'try.html')  


def tracking_table(request):
    products = Product.objects.all()
    return render(request, 'tracking_table.html', {'products': products})



#mainitems
# Render the list of main items
# def item_list(request):
#     items = MainItem.objects.all()
#     return render(request, 'items.html', {'mitem': items})

# # Handle editing of a main item
# def edit_item(request):
#     if request.method == 'POST':
#         item_id = request.POST.get('id')
#         item = get_object_or_404(Item, id=item_id)
#         form = ItemForm(request.POST, instance=item)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Item updated successfully!')
#             return redirect('item_list')
#     return redirect('item_list')

# # Handle deletion of a main item
# def delete_item(request):
#     if request.method == 'POST':
#         item_id = request.POST.get('id')
#         item = MainItem.objects.get(id=item_id)
#         item.delete()
#         messages.success(request, 'Item deleted successfully!')
    
#     # Redirect back to the item list page (items.html)
#     return redirect('item_list')

# #add item
# def add_item(request):
#     if request.method == 'POST':
#         form = AddItemForm(request.POST)
#         if form.is_valid():
#             # Save the form data to the database
#             form.save()
#             # Redirect to a success page or any other page
#             return redirect('items_list')  # Assuming you have a URL pattern named 'items_list' for displaying the list of items
#     else:
#         form = AddItemForm()
#     return render(request, 'add_item.html', {'form': form})



#new
#mainitems
# Render the list of main items
def item_list(request):
    items = MainItem.objects.all()
    return render(request, 'items.html', {'mitem': items})

# Handle editing of a main item
def edit_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')
        item = get_object_or_404(MainItem, id=item_id)
        form = MainItemForm(request.POST, instance=item)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Changes saved successfully.')
            return redirect('item_list')
        else:
            messages.error(request, 'Failed to save changes. Please check the form.')
            for field, errors in form.errors.items():
                messages.error(request, f"{field}: {', '.join(errors)}")
  
    return redirect('item_list')
    
# Handle deletion of a main item
def delete_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')
        item = MainItem.objects.get(id=item_id)
        item.delete()
        messages.success(request, 'Item deleted successfully!')
    
    # Redirect back to the item list page (items.html)
    return redirect('item_list')


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


#add manufacturer
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
    


    #am-provider
def add_amc_provider(request):
    if request.method == 'POST':
        form = AMCProviderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Redirect to a success URL after saving the form
    else:
        form = AMCProviderForm()
    return render(request, 'add_amc_provider.html', {'form': form})

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


def index(request):
    return render(request,'index.html')

def items(request):
    return render(request,'items.html')

def manufacturer(request):
    return render(request,'manufacturer.html')

def tracking(request):
    return render(request,'tracking.html')
 
def manufacturer_list(request):
    manufacturers = Manufacturer.objects.all()
    return render(request, 'manufacturer_list.html', {'manufacturers': manufacturers})




def get_sr_numbers(request):
    lab_id = request.GET.get('lab_id')
    main_item = request.GET.get('main_item')
    manufacturer = request.GET.get('manufacturer')

    if lab_id and main_item and manufacturer:
        sr_numbers = Product.objects.filter(
            lab_name__id=lab_id,
            main_item__name=main_item,
            main_item__manufacturer__name=manufacturer
        ).values_list('sr_no', flat=True).distinct()
        sr_numbers_list = list(sr_numbers)
        return JsonResponse({'sr_numbers': sr_numbers_list})
    return JsonResponse({'sr_numbers': []})


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





#amc-provider
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

    # Pass the data to the template
    context = {
        'letters': letters
    }

    # Render the template with the provided context
    return render(request, 'table.html', context)


def letter_detail(request, letter_id):
    # Fetch the letter
    letter = get_object_or_404(Letter, id=letter_id)
    
    # Get all subproducts associated with the letter
    subproducts = Subproduct.objects.filter(letters=letter).distinct()
    
    # Get the product associated with the first subproduct (assuming all subproducts have the same product)
    product = subproducts.first().product if subproducts.exists() else None

    # Get the current date
    current_date = timezone.now()

    return render(request, 'letter1.html', {
        'product': product,
        'letters': [letter],  # Wrap the single letter in a list to maintain template structure
        'subproducts': subproducts,
        'current_date': current_date
    })


def quotation_form(request):
    letters = Letter.objects.all()
    return render(request, 'letter_intermidiate.html', {'letters': letters})



def quotation_page(request, letter_id):
    letter = get_object_or_404(Letter, pk=letter_id)
    subproducts = letter.subproducts.all()
    
    # Find the product associated with the subproduct
    product = None
    for subproduct in subproducts:
        if subproduct.product:
            product = subproduct.product
            break
    
    amc_providers_exist = set(AMCProvider.objects.values_list('name', flat=True))
    return render(request, 'quotation_info.html', {'letter': letter, 'product': product, 'subproducts': subproducts, 'amc_providers_exist': amc_providers_exist})



def product_list4(request):
    letters = Letter.objects.all()
    return render(request, 'table2.html', {'letters': letters})


def letter_detail4(request, letter_id):
    # Fetch the letter
    letter = get_object_or_404(Letter, id=letter_id)
    subproducts = letter.subproducts.all()
    # Get the product associated with the first subproduct (assuming all subproducts have the same product)
    product = None
    for subproduct in subproducts:
        if subproduct.product:
            product = subproduct.product
            break
    

    # Get the AMC provider for the first subproduct
    amc_provider = letter.subproducts.first().amc_provider if letter.subproducts.exists() else None

    # Get all related subproducts for the product and AMC provider
    related_subproducts = Subproduct.objects.filter(product=product, amc_provider=amc_provider)

    # Accessing service report date from the product's service reports
    service_report_date = None
    if product and product.service_reports.exists():
        service_report_date = product.service_reports.latest('service_date').service_date

    return render(request, 'letter4.html', {
        'product': product,
        'amc_provider': amc_provider,
        'related_subproducts': related_subproducts,
        'service_report_date': service_report_date,
        'letter': letter
    })




def letter_detail6(request, letter_id):
    letter = get_object_or_404(Letter, pk=letter_id)
    subproducts = letter.subproducts.select_related('amc_provider', 'product')
    product = subproducts.first().product if subproducts else None
    main_item = product.main_item if product else None
    quotations = Quotation.objects.filter(
        product=product,
        quotationitem__subproduct__in=subproducts
    ).distinct() if product else []

    # Calculate global variables
    global_total_basic_price = Decimal('0')
    global_gst_value = Decimal('0')
    global_total_price_inclusive = Decimal('0')

    # Group subproducts by amc_provider name
    grouped_subproducts = {}
    amc_providers = set()
    for sub in subproducts:
        provider_name = sub.amc_provider.name if sub.amc_provider else 'Unknown'
        if provider_name not in grouped_subproducts:
            grouped_subproducts[provider_name] = []
        grouped_subproducts[provider_name].append(sub)

        # Collect unique AMC providers
        amc_providers.add(sub.amc_provider)

        # Fetch the related QuotationItem
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
                "भाग, उपसाधने व इतर वस्तू साधनसामग्री विकत घेण्यासाठी मंजूरी देणे करितासंयत्रे , यंत्रसामग्री आणि "
                "साधनसामग्री इत्यादीच्या दुरुस्ती करिता वार्षिक खर्च यंत्रसामग्रीच्या पुस्तकी किंमतीच्या 25% "
                "मर्यादेपर्यंत विभाग प्रमुख व प्रादेशिक कार्यालय प्रमुख यांना दरपत्रक मागून सुट्ट्या भागांची खरेदी "
                "करण्याबाबत अधिकार आहेत."
            )

    return render(request, 'letter6.html', {
        'letter': letter,
        'main_item': main_item,  # Pass main_item to the template
        'product': product,
        'grouped_subproducts': grouped_subproducts,
        'global_total_basic_price': global_total_basic_price,
        'quotations': quotations,
        'global_gst_value': global_gst_value,
        'global_total_price_inclusive': global_total_price_inclusive,
        'quotation_expense_criteria_text': quotation_expense_criteria_text,
        'unique_amc_providers': amc_providers,  # Pass the set of unique AMC providers
    })
    
    
def product_list6(request):
    letters = Letter.objects.all()
    return render(request, 'table6.html', {'letters': letters})


def product_list7(request):
    letters = Letter.objects.all()
    return render(request, 'table7.html', {'letters': letters})

def letter_detail7(request, letter_id):
    # Fetch the letter using letter_id
    letter = get_object_or_404(Letter, pk=letter_id)
    # Get the subproducts associated with the letter
    subproducts = letter.subproducts.all()

    # Fetch the product(s) associated with these subproducts
    product_ids = subproducts.values_list('product', flat=True).distinct()
    products = Product.objects.filter(id__in=product_ids)

    # For simplicity, assume all subproducts belong to the same product
    product = products.first() if products.exists() else None

    # Fetch all quotations related to these products
    quotations = Quotation.objects.filter(product__in=products).distinct()

    # Group the subproducts by their AMC providers
    grouped_subproducts = {}
    for subproduct in subproducts:
        provider_name = subproduct.amc_provider.name
        if provider_name not in grouped_subproducts:
            grouped_subproducts[provider_name] = []
        grouped_subproducts[provider_name].append(subproduct)

    return render(request, 'letter.html', {
        'letter': letter,
        'product': product,
        'grouped_subproducts': grouped_subproducts,
        'quotations': quotations
    })
@csrf_exempt
def submit_form(request):
    if request.method == 'POST':
        try:
            # Get form data
            letter_no = request.POST.get('letter_no')
            lab_name_id = request.POST.get('lab_name')
            letter_date = request.POST.get('date')

            if not lab_name_id.isdigit():
                raise ValueError(f"lab_name_id is not a digit: {lab_name_id}")

            # Validate and parse the date
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

            # Process products and their subproducts
            product_index = 0
            while True:
                sr_no = request.POST.get(f'products[{product_index}][sr_no]')
                service_report_date = request.POST.get(f'products[{product_index}][service_report_date]')

                if not sr_no:
                    break

                # Find the product by SR No
                try:
                    product = Product.objects.get(sr_no=sr_no)
                    amc_provider = product.amc_provider  # Assume AMC provider is a field in the Product model
                except Product.DoesNotExist:
                    raise ValueError(f"Product with SR No {sr_no} does not exist")

                # Validate and parse the service report date if provided
                if service_report_date:
                    try:
                        service_report_date = datetime.datetime.strptime(service_report_date, '%Y-%m-%d').date()
                    except ValueError:
                        raise ValueError(f"Service report date {service_report_date} is not in the correct format YYYY-MM-DD")

                    # Update service report date
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

                    if not part_quantity.isdigit():
                        raise ValueError(f"Part quantity is not a digit: {part_quantity}")

                    # Create a Subproduct instance
                    subproduct = Subproduct.objects.create(
                        product=product,
                        part_name=part_name,
                        type_of_part=part_type,
                        specification=part_specification,
                        quantity=int(part_quantity),
                        amc_provider=amc_provider  # Use AMC provider from the Product model
                    )

                    # Add subproduct to the letter
                    letter.subproducts.add(subproduct)

                    subproduct_index += 1

                product_index += 1

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


@csrf_exempt
def submit_quotation_info(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        date = request.POST.get('date')
        ref_no = request.POST.get('ref_no')
        quotation_expense_criteria = request.POST.get('quotation_criteria')

        # Create the quotation
        product = Product.objects.get(pk=product_id)
        total_price = 0  # Initialize total_price

        # Process each subproduct
        subproduct_ids = [key.split('_')[-1] for key in request.POST.keys() if key.startswith('subproduct_id')]
        for subproduct_id in subproduct_ids:
            subproduct = Subproduct.objects.get(pk=subproduct_id)
            unit_price = Decimal(request.POST.get(f'unit_price_{subproduct_id}'))  # Convert to Decimal
            quantity = subproduct.quantity
            price_without_gst = unit_price * quantity
            gst_value = price_without_gst * Decimal('0.18')  # Calculate GST value
            price_with_gst = price_without_gst + gst_value

            total_price += price_with_gst  # Add price_with_gst to total_price

        # Check if total price exceeds expenditure cost limit
        if product.expenditure_cost - total_price < 0:
            return JsonResponse({'message': 'Expenditure cost limit exceeded. Quotation cannot be submitted.'}, status=400)

        # Create the quotation
        quotation = Quotation.objects.create(
            product=product,
            quotation_date=date,
            ref_no=ref_no,
            quotation_expense_criteria=quotation_expense_criteria
        )

        # Process each subproduct and create quotation items
        for subproduct_id in subproduct_ids:
            subproduct = Subproduct.objects.get(pk=subproduct_id)
            amc_provider = subproduct.amc_provider
            unit_price = Decimal(request.POST.get(f'unit_price_{subproduct_id}'))  # Convert to Decimal
            quantity = subproduct.quantity
            price_without_gst = unit_price * quantity
            gst_value = price_without_gst * Decimal('0.18')  # Calculate GST value
            price_with_gst = price_without_gst + gst_value

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

        # Update total_price and save quotation
        quotation.total_price = total_price
        quotation.save()

        return JsonResponse({'message': 'Quotation information submitted successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)