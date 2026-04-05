from rest_framework import serializers
from .models import Order, OrderItem, Payment


class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'unit_price', 'quantity', 'subtotal']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'method', 'status', 'transaction_id', 'amount', 'paid_at']
        read_only_fields = ['status', 'paid_at']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    payment = PaymentSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'status', 'total_amount', 'shipping_address',
            'notes', 'items', 'payment', 'created_at'
        ]
        read_only_fields = ['status', 'total_amount']


class PlaceOrderSerializer(serializers.Serializer):
    """
    Used ONLY when placing a new order.
    Validates the input before we process the cart.
    """
    shipping_address_id = serializers.IntegerField()
    payment_method = serializers.ChoiceField(choices=[
        'credit_card', 'paypal', 'stripe', 'bank_transfer'
    ])
    notes = serializers.CharField(required=False, allow_blank=True)