from django.db import models
from django.db.models import Q
from django.db import transaction
from django.utils.text import slugify
import logging
logger = logging.getLogger(__name__)


class Category(models.Model):
    """
    Product categories (e.g., Electronics, Clothing).
    Supports sub-categories via the parent field (self-referential).
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)            # URL-friendly name: "electronics"
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    parent = models.ForeignKey(
        'self',                                     # Points to itself = sub-category
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='children'
    )

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        # Auto-generate slug from name
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Main product table."""
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, related_name='products'
    )
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True
    )
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True)    # Stock Keeping Unit
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def effective_price(self):
        """Return discount price if available, otherwise regular price."""
        return self.discount_price if self.discount_price else self.price

    @property
    def in_stock(self):
        return self.stock > 0

    def __str__(self):
        return self.name



class ProductImage(models.Model):
    """A product can have multiple images."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product'],
                condition=Q(is_primary=True),
                name='unique_primary_image_per_product'
            )
        ]
        ordering = ['order']

    def save(self, *args, **kwargs):
        print(f"Saving ProductImage: product={self.product.name}, is_primary={self.is_primary}")
        logger.warning(f"Saving ProductImage: product={self.product.name}, is_primary={self.is_primary}")
        with transaction.atomic():
            if self.is_primary:
                ProductImage.objects.filter(
                    product=self.product,
                    is_primary=True
                ).exclude(pk=self.pk).update(is_primary=False)

            super().save(*args, **kwargs)
    def __str__(self):
        return f"Image for {self.product.name}"