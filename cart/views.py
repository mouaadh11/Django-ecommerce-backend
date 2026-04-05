from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product


def get_or_create_cart(user):
    """Helper: get user's cart or create it if it doesn't exist."""
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


class CartView(APIView):
    """GET /api/cart/ — View the current user's cart."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart = get_or_create_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartItemView(APIView):
    """POST /api/cart/items/ — Add or update item in cart."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart = get_or_create_cart(request.user)
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))

        # Validate product exists
        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check stock
        if product.stock < quantity:
            return Response(
                {'error': f'Only {product.stock} items available.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Add or update cart item
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity   # Add to existing quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, item_id):
        """DELETE /api/cart/items/<item_id>/ — Remove item from cart."""
        cart = get_or_create_cart(request.user)
        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
            item.delete()
            return Response({'message': 'Item removed.'}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, item_id):
        """PATCH /api/cart/items/<item_id>/ — Update quantity."""
        cart = get_or_create_cart(request.user)
        quantity = request.data.get('quantity')

        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)

        if int(quantity) < 1:
            item.delete()
        else:
            item.quantity = quantity
            item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data)