from django.shortcuts import render, HttpResponse
from product.models import Product

def home(request):
    return render(request, 'index.html')

def details(request, code):
    product = Product.objects.get(code=code)
    return render(request, 'details.html', context={'product': product})