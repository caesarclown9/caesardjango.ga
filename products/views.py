from rest_framework import generics
from rest_framework.response import Response

from .serializers import ProductSerializer
from .models import Product

class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
