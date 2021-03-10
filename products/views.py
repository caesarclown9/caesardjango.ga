from datetime import timedelta

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils import timezone
from rest_framework import generics
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action

from . import models
from . import permissions
from .serializers import ProductSerializer
from order.permissions import IsAuthor

class MyPaginationClass(PageNumberPagination):
    page_size = 2

    def get_paginated_response(self, data):
        return super().get_paginated_response(data=data)

class ProductCreateAPIView(generics.CreateAPIView):
    permission_classes = (permissions.IsSeller,)
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthorOrReadOnly, )
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer



class ProductListAPIView(generics.ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = MyPaginationClass

    def get_queryset(self):
        value = self.request.query_params.get('value')
        queryset = super().get_queryset()
        if value:
            value_from, value_to = value.split('-')
            queryset = queryset.filter(value__gt=value_from, value__lt=value_to)
        return queryset


class AuthorsProductListAPIView(generics.ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthor, )
    pagination_class = MyPaginationClass

    def get_queryset(self):
        return models.Product.objects.filter(author=self.request.user)


class SearchListView(generics.ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = MyPaginationClass

    def get_queryset(self, *args, **kwargs):
        search = self.request.query_params.get('search')
        queryset = super().get_queryset()
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(body__icontains=search))
        return queryset



