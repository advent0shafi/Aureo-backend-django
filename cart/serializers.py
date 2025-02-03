from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerializer  # Import your ProductSerializer
from products.models import Product  # Import your Product model

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True,
        source='product'
    )
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'id',
            'product_id',
            'product',
            'quantity',
            'subtotal',
            'added_at',
            'price',
            'currency',
            'material',
            'diamond_weight',
            'diamond_quality',
            'sku',
        ]
        read_only_fields = [
            'id',
            'product',
            'subtotal',
            'added_at',
            'price',
            'currency',
            'material',
            'diamond_weight',
            'diamond_quality',
            'sku',
        ]

    def get_subtotal(self, obj):
        return obj.subtotal  # Use the subtotal property of CartItem

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()
    shipping_cost = serializers.SerializerMethodField()
    vat = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'guest_id',
            'items',
            'total',
            'subtotal',
            'shipping_cost',
            'vat',
            'total_items',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'user',
            'total',
            'subtotal',
            'shipping_cost',
            'vat',
            'total_items',
            'created_at',
            'updated_at',
        ]

    def get_total(self, obj):
        return obj.total  # Use the total property of Cart

    def get_subtotal(self, obj):
        return obj.subtotal  # Use the subtotal property of Cart

    def get_shipping_cost(self, obj):
        return obj.shipping_cost  # Use the shipping_cost property of Cart

    def get_vat(self, obj):
        return obj.vat  # Use the vat property of Cart

    def get_total_items(self, obj):
        return obj.total_items  # Use the total_items property of Cart