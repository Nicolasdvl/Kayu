
from rest_framework import generics
from product.models import Product, Category
from product.serializers import ProductSerializer, CategorySerializer
from rest_framework import filters


class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        print(request.query_params)
        if request.query_params.get('fields'):
            fields = request.query_params.get('fields').split(',')
            return [field for field in fields if field in [field.name for field in Product._meta.fields]]
        return super().get_search_fields(view, request)

class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [CustomSearchFilter]
    search_fields = ['name',]


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    