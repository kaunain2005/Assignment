from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    # return HttpResponse("Welcome to My Company!")
    return render(request, 'website/index.html')
