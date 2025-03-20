# serializers.py
from rest_framework import serializers
from .models import Category, Product, Variant
from .models import ProductPrice

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'subcategories']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)

    class Meta:
        model = Product
        fields = ['id', 'category', 'category_id', 'name', 'description',  'image']
        


class ProductPriceSerializer(serializers.ModelSerializer):
    formatted_price = serializers.CharField( read_only=True)

    class Meta:
        model = ProductPrice
        fields = ['id', 'product', 'text', 'quantity', 'price', 'formatted_price']


class VariantSerializer(serializers.ModelSerializer):
    product = serializers.IntegerField(source='product.id', read_only=True)

    class Meta:
        model = Variant
        fields = ['id', 'product', 'name', 'price', 'image']


# admin.py

