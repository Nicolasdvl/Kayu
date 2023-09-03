
from rest_framework import generics, filters
from product.models import Product, Category
from product.serializers import ProductSerializer, CategorySerializer
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse


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

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    