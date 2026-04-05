from rest_framework import generics, permissions
from .models import Review
from .serializers import ReviewSerializer


class ProductReviewListView(generics.ListCreateAPIView):
    """
    GET  /api/reviews/?product=<id> — List reviews for a product
    POST /api/reviews/              — Submit a review (must be logged in)
    """
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        product_id = self.request.query_params.get('product')
        if product_id:
            return Review.objects.filter(product_id=product_id)
        return Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PATCH/DELETE /api/reviews/<id>/ — Manage own review."""
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)  # Can only edit own reviews