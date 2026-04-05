from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductReviewListView.as_view(), name='review-list'),
    path('<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
]