from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name


class ProductPrice(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='prices')
    text = models.CharField(max_length=255) 
    quantity = models.PositiveIntegerField()  # New field to store quantity
    price = models.IntegerField()  # Changed from DecimalField to IntegerField

    def formatted_price(self):
        """Returns the price formatted with commas (e.g., 1,000 or 10,000)."""
        return f"{self.price:,}"

    def __str__(self):
        return f"{self.product.name} - {self.description}: {self.formatted_price()}"



class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='variants/', null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.name}"
