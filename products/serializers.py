from rest_framework import serializers

from .models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = [
            'author', 'created_at', 'updated_at'
        ]


class CategoryAPISerializer(serializers.ModelSerializer):
    products = serializers.StringRelatedField(many=True)

    class Meta:
        model = Category
        fields = [
            'id', 'title', 'products'
        ]

