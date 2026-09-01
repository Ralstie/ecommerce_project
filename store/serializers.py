"""Serializers used by the eCommerce REST API."""

from rest_framework import serializers

from .models import Store, Product, Review


class StoreSerializer(serializers.ModelSerializer):
    """Serialize store data and assign the authenticated vendor as owner."""

    vendor = serializers.ReadOnlyField(source='vendor.username')

    class Meta:
        model = Store
        fields = ['id', 'vendor', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'vendor', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    """Serialize product data and expose the owning store as a read-only field."""

    store_name = serializers.ReadOnlyField(source='store.name')

    class Meta:
        model = Product
        fields = [
            'id', 'store', 'store_name', 'name', 'description',
            'price', 'stock', 'image', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'store_name', 'created_at', 'updated_at']

    def validate_store(self, store):
        """Ensure a vendor can only add products to their own store."""
        request = self.context.get('request')
        if request and store.vendor != request.user:
            raise serializers.ValidationError(
                'You can only add products to your own store.'
            )
        return store


class ReviewSerializer(serializers.ModelSerializer):
    """Serialize product review information for API consumers."""

    buyer = serializers.ReadOnlyField(source='buyer.username')
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = Review
        fields = [
            'id', 'buyer', 'product', 'product_name', 'rating',
            'comment', 'verified', 'created_at'
        ]
        read_only_fields = [
            'id', 'buyer', 'product_name', 'verified', 'created_at'
        ]
