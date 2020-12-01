from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from . import models
from . import permissions
from . import serializers
from order.permissions import IsAuthor


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
    serializer_class = serializers.ProductSerializer
    permission_classes = (IsAuthor, )

    def get_queryset(self):
        return models.Product.objects.filter(author=self.request.user)


class WishListApiView(generics.ListCreateAPIView):
    serializer_class = serializers.WishAPISerializer

    def get_queryset(self):
        queryset = Wish.objects.all()
        return Wish.objects.filter(user=self.request.user.id)

    def post(self, request, *args, **kwargs):
        if len(request.data.keys()) == 1 and request.data.get('product'):
            user = request.user.id
            product = request.data['product']
            favorites = Wish.objects.filter(product=product, user=user.id)
            if favorites:
                raise serializers.ValidationError('Product in WishList')
            request.data['user'] = request.user.id

        else:
            raise serializers.ValidationError('Error')
            pass
        return self.create(request, *args, **kwargs)


class WishAdd(APIView):

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        user = request.user
        url = request.build_absolute_uri()
        if Wish.objects.filter(user=user.id, product=pk):
            raise serializers.ValidationError('OK')
        new_favorite = Wish.objects.create(user=user, product=product)
        return HttpResponseRedirect(redirect_to=url)


class WishDelete(APIView):

    def get(self, request, pk):
        user = request.user
        print(user)
        product = Product.objects.get(pk=pk)

        favor = Wish.objects.filter(user=user.id, product=pk)
        print(favor)
        if favor:
            favor.delete()
            raise serializers.ValidationError('Deleted!')
        raise serializers.ValidationError('Not Found!')
