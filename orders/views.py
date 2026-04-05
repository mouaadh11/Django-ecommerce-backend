from django.utils import timezone
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order, OrderItem, Payment
from .serializers import OrderSerializer, PlaceOrderSerializer
from cart.models import Cart
from users.models import Address


class PlaceOrderView(APIView):
    """
    POST /api/orders/
    This is the checkout endpoint. It:
    1. Validates the cart isn't empty
    2. Validates the shipping address exists
    3. Creates an Order from the cart contents
    4. Creates OrderItems (with price snapshots)
    5. Creates a Payment record
    6. Clears the cart
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PlaceOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found.'}, status=status.HTTP_400_BAD_REQUEST)

        if not cart.items.exists():
            return Response({'error': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate address belongs to this user
        try:
            address = Address.objects.get(
                id=serializer.validated_data['shipping_address_id'],
                user=request.user
            )
        except Address.DoesNotExist:
            return Response({'error': 'Address not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check all items are still in stock
        for item in cart.items.all():
            if item.product.stock < item.quantity:
                return Response(
                    {'error': f'"{item.product.name}" has only {item.product.stock} items in stock.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Create the order
        order = Order.objects.create(
            user=request.user,
            total_amount=cart.total_price,
            shipping_address={   # Snapshot: save address as JSON
                'full_name': address.full_name,
                'street_line1': address.street_line1,
                'street_line2': address.street_line2,
                'city': address.city,
                'state': address.state,
                'postal_code': address.postal_code,
                'country': address.country,
            },
            notes=serializer.validated_data.get('notes', '')
        )

        # Create order items & reduce stock
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                unit_price=item.product.effective_price,
                quantity=item.quantity,
            )
            # Reduce stock
            item.product.stock -= item.quantity
            item.product.save()

        # Create payment record
        Payment.objects.create(
            order=order,
            method=serializer.validated_data['payment_method'],
            amount=order.total_amount,
        )

        # Clear the cart
        cart.items.all().delete()

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )


class OrderListView(generics.ListAPIView):
    """GET /api/orders/ — List logged-in user's orders."""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=request.user).prefetch_related('items', 'payment')


class OrderDetailView(generics.RetrieveAPIView):
    """GET /api/orders/<id>/ — Single order details."""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)