from rest_framework import serializers
from product.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'products']


class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['code', 'name', 'brand', 'image', 'nutriscore', 'ingredients', 'categories']

    def get_categories(self, obj):
        categories = [
            CategorySerializer(category).data for category in obj.category_set.all()
        ]
        return categories

         

