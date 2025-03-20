from django.contrib import admin
from .models import Category, Product, Variant, ProductPrice
from django.utils.html import format_html


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']
    search_fields = ['name']
    list_filter = ['parent']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category',  'image_preview']
    list_filter = ['category']
    search_fields = ['name', 'description']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:5px;"/>', obj.image.url)
        return None
    image_preview.short_description = 'Image'
    


@admin.register(ProductPrice)
class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ('product', 'text', 'quantity', 'formatted_price')  # Display formatted price
    list_filter = ('product',)  # Filter by product
    search_fields = ('product__name', 'text')  # Search by product name and text
    ordering = ('product', 'price')  # Order by product and price



@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ['name', 'product', 'price', 'image_preview']
    list_filter = ['product']
    search_fields = ['name']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:5px;"/>', obj.image.url)
        return None
    image_preview.short_description = 'Image'


