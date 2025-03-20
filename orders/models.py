import uuid
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from form.models import Form

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="orders")
    submitted_at = models.DateTimeField(auto_now_add=True)
    field_values = models.JSONField()  # Store submitted form data
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    unique_id = models.CharField(max_length=12, unique=True, editable=False)


    def __str__(self) -> str:
        return f"Order {self.id} - {self.form.name} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        """Generate unique numeric ID before saving"""
        if not self.unique_id:
            self.unique_id = str(int(uuid.uuid4().int))[:7]  # Convert UUID to int and slice first 12 digits
        super().save(*args, **kwargs)


