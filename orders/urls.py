from django.urls import path
from . import views

urlpatterns = [
    path('', views.PlaceOrderView.as_view(), name='place-order'),
    path('list/', views.OrderListView.as_view(), name='order-list'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
]