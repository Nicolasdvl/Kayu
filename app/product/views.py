
from rest_framework import generics, filters, status
from product.models import Product, Category
from product.serializers import ProductSerializer, CategorySerializer
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, BrowsableAPIRenderer
from django.db.models import Count


class UIRenderer(TemplateHTMLRenderer):
    media_type = 'text/html'
    format = 'ui'

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
    renderer_classes = [UIRenderer, JSONRenderer, BrowsableAPIRenderer]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if request.accepted_renderer.format == 'ui':
            return Response(data={'products':queryset}, template_name='product-list.html')
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
    renderer_classes = [UIRenderer, JSONRenderer, BrowsableAPIRenderer]

    def list(self, request, *args, **kwargs):
        self.code = request.query_params.get('product', None)
        if self.code is None:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        queryset = self.filter_queryset(self.get_queryset())
        if request.accepted_renderer.format == 'ui':
            return Response(data={'substitutes':queryset}, template_name='substitutes-list.html')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        categories = Category.objects.filter(products=self.code).annotate(num_products=Count("products")).order_by("num_products")
        category = categories[::-1][0]
        products = Product.objects.filter(category=category)
        return products
    
    def filter_queryset(self, queryset):
        return queryset.order_by("nutriscore")


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    