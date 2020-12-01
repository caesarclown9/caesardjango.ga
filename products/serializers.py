from rest_framework import serializers

from .models import Product, Category, Wish, Bucketlist, BucketlistItem


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

class WishAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Wish
        fields = ('product', 'user')

class BucketlistItemSerializer(serializers.ModelSerializer):
    """
    Serialier class for a bucketlist item
    """

    def create(self, validated_data):
        try:
            if not validated_data.get('item_name'):
                raise serializers.ValidationError('The name cannot be empty')
            return super(BucketlistItemSerializer, self).create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError('That name already exists')

    def update(self, instance, validated_data):
        try:
            return super(BucketlistItemSerializer, self).update(instance, validated_data)
        except IntegrityError:
            raise serializers.ValidationError('That name already exists')

    class Meta:
        model = BucketlistItem
        fields = ('id', 'item_name', 'date_created', 'date_modified', 'is_done')
        read_only_fields = ('id', 'date_created', 'date_modified')


class BucketlistSerializer(serializers.ModelSerializer):
    """
    serializer class for bucketlists
    """
    bucketlist_items = BucketlistItemSerializer(many=True, read_only=True)

    def create(self, validated_data):
        try:
            if not validated_data.get('name'):
                raise serializers.ValidationError('The name cannot be empty')
            return super(BucketlistSerializer, self).create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError('That name already exists')

    def update(self, instance, validated_data):
        try:
            return super(BucketlistSerializer, self).update(instance, validated_data)
        except IntegrityError:
            raise serializers.ValidationError('That name already exists')

    class Meta:
        model = Bucketlist
        fields = ('id', 'name', 'description', 'date_created', 'date_modified', 'bucketlist_items')
        read_only_fields = ('id', 'date_created', 'date_modified','created_by', 'bucketlist_items')