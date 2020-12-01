from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import models
from . import permissions
from . import serializers


class ProductCreateAPIView(generics.CreateAPIView):
    permission_classes = (permissions.IsSeller,)
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthorOrReadOnly, )
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer



class ProductListAPIView(generics.ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


class AuthorsProductListAPIView(generics.ListAPIView):
    queryset = models.Product.objects.all()
    serializers_class = serializers.ProductSerializer
    permission_classes = (IsAuthenticated, permissions.IsSeller, )

    def get_queryset(self):
        return models.Product.objects.filter(author=self.request.user)