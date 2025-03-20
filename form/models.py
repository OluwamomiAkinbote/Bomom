import uuid
from django.db import models
from django.contrib.sites.models import Site
from products.models import Product

class Form(models.Model):
    name = models.CharField(max_length=255)
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="forms", null=True, blank=True)
    head_text = models.TextField(default="Please fill out the form below")
    subheader_text = models.TextField(default="All fields marked with * are required")
    unique_id = models.CharField(max_length=12, unique=True, editable=False)
    embed_code = models.TextField(editable=False)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        """Generate unique ID and embed code before saving"""
        if not self.unique_id:
            self.unique_id = uuid.uuid4().hex[:12].upper()  

        current_site = Site.objects.get_current()
        domain = current_site.domain

        if not self.embed_code:
            self.embed_code = (
                f'<iframe src="https://{domain}/forms/{self.unique_id}/details/" '
                'width="100%" height="600" frameborder="0"></iframe>'
            )

        super().save(*args, **kwargs)

class Section(models.Model):
    name = models.CharField(max_length=255)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="sections")

    def __str__(self) -> str:
        return self.name

class Field(models.Model):
    FIELD_TYPE_CHOICES = [
        ("text", "Text"),
        ("number", "Number"),
        ("email", "Email"),
        ("phone", "Phone"),
        ("radio", "Radio"),
        ("checkbox", "Checkbox"),
        ("select", "Select"),
    ]
    label = models.CharField(max_length=255)
    field_type = models.CharField(max_length=50, choices=FIELD_TYPE_CHOICES)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="form_fields")
    placeholder = models.CharField(max_length=255, blank=True, null=True)
    is_required = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.label} ({'Required' if self.is_required else 'Optional'})"

class FieldChoice(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.choice_text


