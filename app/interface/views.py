from django.shortcuts import render, HttpResponse
from product.views import ProductList

def home(request):
    print(request)
    return render(request, 'index.html')

