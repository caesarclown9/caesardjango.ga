from rest_framework import serializers
from .models import Product, Category, Balance


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


class BalanceAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ['balance']
