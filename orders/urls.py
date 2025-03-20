from django.urls import path
from .views import OrderView, OrderDetailView

urlpatterns = [
    path("orders/", OrderView.as_view(), name="order-list-create"),  # List & Create Orders
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),  # Retrieve & Update Order
]
