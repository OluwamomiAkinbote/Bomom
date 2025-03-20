from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "form", "submitted_at", "field_values", "status", "unique_id"]
        read_only_fields = ["unique_id"]  # Ensures unique_ids cannot be modified
