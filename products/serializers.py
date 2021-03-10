from rest_framework import serializers

from .models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id','title', 'body', 'value', 'qty', 'category', 'image'
        ]



class CategoryAPISerializer(serializers.ModelSerializer):
    products = serializers.StringRelatedField(many=True)

    class Meta:
        model = Category
        fields = [
            'id', 'title', 'products'
        ]
