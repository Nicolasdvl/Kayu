
from rest_framework import generics, filters
from product.models import Product, Category
from product.serializers import ProductSerializer, CategorySerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count


class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('fields'):
            fields = request.query_params.get('fields').split(',')
            return [field for field in fields if field in [field.name for field in Product._meta.fields]]
        return super().get_search_fields(view, request)

class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [CustomSearchFilter]
    search_fields = ['name','code']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if 'UI' in request.query_params :
            result = []
            content = render(request, 'result.html', context={'products': queryset})
            return HttpResponse(content, content_type='text/html')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ProductDetail(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        code = self.kwargs['code']
        return Product.objects.filter(code=code)


class ProductSubstitutes(generics.ListAPIView):
    serializer_class = ProductSerializer
    ordering = ['nutriscore']

    def get_queryset(self):
        code = self.request.query_params.get('product')
        categories = Category.objects.filter(products=code).annotate(num_products=Count("products")).order_by("num_products")
        category = categories[0]
        products = Product.objects.filter(category=category)
        return products
    
    def filter_queryset(self, queryset):
        return queryset.order_by("nutriscore")


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    