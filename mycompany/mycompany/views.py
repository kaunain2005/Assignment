from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    # return HttpResponse("Welcome to My Company!")
    return render(request, 'website/index.html')

def about(request):
    return HttpResponse("About My Company")

def contact(request):
    return HttpResponse("Contact My Company at contact@mycompany.com")