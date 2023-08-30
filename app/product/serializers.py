from rest_framework import serializers
from product.models import Product, Category

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['code', 'name', 'brand', 'image', 'nutriscore', 'ingredients']