from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def say_hello(request):
    return render(request,'index.html',{'name':'Samarth'})

def load_vendorInfo(request):
    return render(request,'vendor information.html')

def load_vendorId(request):
    return render(request,'vendor_identifier.html')

def load_vendorBankDetails(request):
    return render(request,'vendorBank.html')
