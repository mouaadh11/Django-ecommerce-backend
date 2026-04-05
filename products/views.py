from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product
from .serializers import CategorySerializer, ProductListSerializer, ProductDetailSerializer
from .filters import ProductFilter


class CategoryListView(generics.ListAPIView):
    """GET /api/products/categories/ — List all categories."""
    queryset = Category.objects.filter(parent=None)   # Top-level only
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductListView(generics.ListAPIView):
    """
    GET /api/products/
    Supports: ?search=laptop&category=1&min_price=100&max_price=500&ordering=price
    """
    queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']


class ProductDetailView(generics.RetrieveAPIView):
    """GET /api/products/<slug>/ — Single product full details."""
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'   # Use slug in URL instead of ID