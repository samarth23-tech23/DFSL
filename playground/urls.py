from django.urls import path
from . import views
urlpatterns = [
    path('hello/',views.say_hello ),
    path('vendorInfo/',views.load_vendorInfo),
    path('vendorId/',views.load_vendorId),
    path('vendorBank/',views.load_vendorBankDetails),   
    
]
