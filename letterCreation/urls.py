from django.urls import path
from . import views

urlpatterns = [
    

    path('tracking_table/', views.tracking_table, name='tracking_table'),

    path('',views.index),
    path('update-print-date/', views.update_print_date, name='update_print_date'),
    path('track-letter/<int:letter_id>/', views.track_letter, name='track_letter'),

#main items
   path('items/', views.items_list, name='items_list'),
    path('add/', views.add_item, name='add_item'),
    path('edit/<int:item_id>/', views.edit_item, name='edit_item'),    
    path('delete/', views.delete_item, name='delete_item'),

# delete
      path('delete/', views.delete_item, name='delete_item'),


    path('tracking/',views.tracking_table,  name='tracking_table'),
    path('get_service_report_dates/<int:product_id>/', views.get_service_report_dates, name='get_service_report_dates'),

    # path('tracking_table/', views.tracking, name='tracking_table'),

    path('form/',views.load_form), 
   
    
    path('get_sr_numbers/', views.get_sr_numbers, name='get_sr_numbers'),

   

#manufacturer
    path('manufacturer/', views.manufacturer_view, name='manufacturer'), 
    path('edit/<int:manufacturer_id>/', views.edit_manufacturer, name='edit_manufacturer'),
     path('get_manufacturers/', views.get_manufacturers, name='get_manufacturers'),
    path('manufacturer/', views.manufacturer_list, name='manufacturer_list'),
    
    path('get_manufacturer_names/', views.get_manufacturer_names, name='get_manufacturer_names'),
   
    path('edit/<int:id>/', views.edit_manufacturer, name='edit_manufacturer'),

    # add manufacturer
    path('add_manufacturer/', views.add_manufacturer, name='add_manufacturer'),

# delete manufacturer
    path('delete-manufacturer/', views.delete_manufacturer, name='delete_manufacturer'),

#product_list
    path('product_list/', views.product_list_view, name='product_list_view'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('add_product/', views.add_product_view, name='add_product_view'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('product/<int:product_id>/json/', views.product_detail_json, name='product_detail_json'),
    path('get_departments/', views.get_departments, name='get_departments'),

#amcproviders     
    path('amc-providers/', views.amc_providers_list, name='amc_providers_list'),
    path('edit_amc_provider/<int:id>/', views.edit_amc_provider, name='edit_amc_provider'),
    path('delete_amc_provider/<int:id>/', views.delete_amc_provider, name='delete_amc_provider'),
    path('confirm_delete_amc_provider/<int:id>/', views.confirm_delete_amc_provider, name='confirm_delete_amc_provider'),
    path('add_amc_provider/', views.add_amc_provider, name='add_amc_provider'),

#service-report-history
    path('service-report-history/', views.service_report_history, name='service_report_history'),


   path('submit_form/', views.submit_form, name='submit_form'),

#letter 3
    path('products/', views.product_list, name='product_list'),
    path('products/<int:letter_id>/', views.letter_detail, name='letter_detail'),
 

#Quotations
    path('quotations/', views.quotation_form, name='product_list3'),
    path('submit_quotation_info/', views.submit_quotation_info, name='submit_quotation_info'),
    path('quotations/<int:letter_id>/', views.quotation_page, name='quotation_page'),

    ###################
#letter 4
    path('products4/', views.product_list4, name='product_list2'),
    path('products4/<int:letter_id>/', views.letter_detail4, name='letter_detail4'),

#letter 6
    path('products6/', views.product_list6, name='product_list6'),
    path('letter6/<int:letter_id>/', views.letter_detail6, name='letter_detail6'),


#letter 7
    path('products7/', views.product_list7, name='product_list7'),
    path('products7/<int:letter_id>/', views.letter_detail7, name='letter_detail7'),



]