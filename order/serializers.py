from rest_framework import serializers

from .models import Order, OrderItem
from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class OrderItemDetailSerializer(serializers.ModelSerializer):

    product = ProductSerializer('product')

    class Meta:
        model = OrderItem
        fields = ['product', 'order']


class OrderItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['product', 'order']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'address', 'city',
    ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['products'] = OrderItemDetailSerializer(instance.orderitems.all(), many=True).data
        return representation


