from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "form", "status", "submitted_at", "order_id")
    list_filter = ("status", "submitted_at")
    search_fields = ("form__name",)  # Ensure 'name' exists in Form model
    ordering = ("-submitted_at",)
    readonly_fields = ("unique_id",)  # Prevent editing unique ID

    @admin.display(description="Unique ID")
    def order_id(self, obj):
        """Show the unique ID in the admin panel."""
        return obj.unique_id if obj.unique_id else "No ID"


