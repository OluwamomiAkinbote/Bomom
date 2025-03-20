from django.contrib import admin
from .models import Form, Section, Field, FieldChoice


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "product_name", "unique_id", "embed_code")
    readonly_fields = ("unique_id", "embed_code")  
    search_fields = ("name", "unique_id", "product_name__name")
    list_filter = ("product_name",)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "form")
    search_fields = ("name", "form__name")
    list_filter = ("form",)


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ("id", "label", "field_type", "section", "placeholder", "is_required", "is_visible")
    search_fields = ("label", "field_type", "section__name")
    list_filter = ("field_type", "is_required", "is_visible", "section")


@admin.register(FieldChoice)
class FieldChoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "choice_text", "field")
    search_fields = ("choice_text", "field__label")
    list_filter = ("field",)
