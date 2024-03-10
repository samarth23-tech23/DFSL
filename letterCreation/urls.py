from django.urls import path
from . import views
urlpatterns = [
    path('hello/',views.say_hello ),
    path('vendorInfo/',views.load_vendorInfo),
    path('vendorId/',views.load_vendorId),
    path('vendorBank/',views.load_vendorBankDetails),   
    path('letter/',views.load_letter),  
    path('letter1/',views.load_letter1),  
    path('letter4/',views.load_letter4),  
    path('form/',views.load_form), 
    path('submit_form/', views.submit_form, name='submit_form'),

#letter 3
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.letter_detail, name='letter_detail'),
    path('demo/',views.load_demo),

#Quotations
    path('quotations/', views.quotation_form, name='product_list3'),
    path('submit_quotation_info/', views.submit_quotation_info, name='submit_quotation_info'),
    path('quotations/<int:product_id>/', views.quotation_page, name='quotation_page'),

    ###################
#letter 4
    path('products4/', views.product_list4, name='product_list2'),
    path('products4/<int:subproduct_id>/', views.letter_detail4, name='letter_detail4'),

#letter 6
    path('products6/', views.product_list6, name='product_list6'),
    path('letter6/<int:subproduct_id>/', views.letter_detail6, name='letter_detail6'),


]
