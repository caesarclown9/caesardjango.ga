from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import models
from . import permissions
from . import serializers


class OrderCreateAPIView(generics.CreateAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        print(dir(self.request.user.order_set))
        # serializer.save(product=self.request)


class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    # permission_classes = permissions.IsAuthor
    