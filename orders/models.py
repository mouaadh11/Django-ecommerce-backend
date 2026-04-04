from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):
    """
    Represents a placed order. Once placed, it goes through
    these statuses in sequence.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),           # Just placed
        ('confirmed', 'Confirmed'),       # Payment received
        ('processing', 'Processing'),     # Being prepared
        ('shipped', 'Shipped'),           # On its way
        ('delivered', 'Delivered'),       # Received by customer
        ('cancelled', 'Cancelled'),       # Cancelled
        ('refunded', 'Refunded'),         # Money returned
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, related_name='orders'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Snapshot of address at time of order (address may change later)
    shipping_address = models.JSONField()

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} by {self.user}"


class OrderItem(models.Model):
    """Each product line in an order — snapshot of price at purchase time."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=300)    # Snapshot: product name may change
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # Snapshot: price may change
    quantity = models.PositiveIntegerField()

    @property
    def subtotal(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product_name}"


class Payment(models.Model):
    """Payment record linked to an order."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=200, blank=True)  # From Stripe/PayPal
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id} — {self.status}"