from rest_framework import serializers
from .models import Form, Section, Field, FieldChoice
import uuid
from django.contrib.sites.models import Site
from products.models import Product


# FieldChoice Serializer
class FieldChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldChoice
        fields = ["id", "choice_text"]


# Field Serializer
class FieldSerializer(serializers.ModelSerializer):
    choices = FieldChoiceSerializer(many=True, required=False)

    class Meta:
        model = Field
        fields = ["id", "label", "field_type", "placeholder", "is_required", "is_visible", "choices"]

    def validate(self, data):
        """
        Check if the field is a phone/WhatsApp field and format the number correctly.
        """
        label = data.get("label", "").strip().lower()
        
        if label in ["phone", "whatsapp"]:
            number = data.get("placeholder", "").strip()  # Assuming placeholder holds the number

            if number.startswith("0"):  
                number = number[1:]  # Remove leading zero
            
            if not number.startswith("+234"):  
                number = "+234" + number  # Add Nigeria's country code

            data["placeholder"] = number  # Save back the formatted number

        return data



# Section Serializer
class SectionSerializer(serializers.ModelSerializer):
    form_fields = FieldSerializer(many=True, required=False)

    class Meta:
        model = Section
        fields = ["id", "name", "form_fields"]


# Form Serializer
class FormSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, required=False)
    unique_id = serializers.ReadOnlyField()
    embed_code = serializers.ReadOnlyField()
    product_name = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Form
        fields = [
            "id", "name", "product_name", "head_text", "subheader_text", 
            "unique_id", "embed_code", "sections"
        ]

    def validate(self, data):
        """Ensure required fields are filled and phone numbers are properly formatted."""
        required_fields = ["name", "head_text", "subheader_text"]

        # Ensure required fields are not empty
        for field in required_fields:
            if not data.get(field) or str(data[field]).strip() == "":
                raise serializers.ValidationError({field: f"{field.replace('_', ' ').capitalize()} cannot be empty."})

        # Format phone numbers
        for section in data.get("sections", []):
            for field in section.get("form_fields", []):
                label = field.get("label", "").lower()
                if "phone" in label or "whatsapp" in label:
                    number = str(field.get("placeholder", "")).strip()
                    if number.startswith("0"):  # Remove leading zero
                        number = number[1:]
                    if not number.startswith("+234"):  # Ensure +234 prefix
                        number = f"+234{number}"
                    field["placeholder"] = number  # Update the field

        return data
    
    def create(self, validated_data):
        """Create a form along with nested sections, fields, and choices."""
        sections_data = validated_data.pop("sections", [])
        form = Form.objects.create(**validated_data)

        # Generate unique ID and embed code
        form.unique_id = uuid.uuid4().hex[:12].upper()
        domain = Site.objects.get_current().domain
        form.embed_code = (
            f'<iframe src="https://{domain}/forms/{form.unique_id}/details/" '
            'width="100%" height="600" frameborder="0"></iframe>'
        )
        form.save()

        # Create sections, fields, and choices
        for section_data in sections_data:
            fields_data = section_data.pop("form_fields", [])
            section = Section.objects.create(form=form, **section_data)

            for field_data in fields_data:
                choices_data = field_data.pop("choices", [])
                field = Field.objects.create(section=section, **field_data)

                for choice_data in choices_data:
                    FieldChoice.objects.create(field=field, **choice_data)

        return form

    def update(self, instance, validated_data):
        """Update the form and its nested objects."""
        sections_data = validated_data.pop("sections", [])

        instance.name = validated_data.get("name", instance.name)
        instance.product_name = validated_data.get("product_name", instance.product_name)
        instance.head_text = validated_data.get("head_text", instance.head_text)
        instance.subheader_text = validated_data.get("subheader_text", instance.subheader_text)
        instance.save()

        # Convert existing sections into a dictionary for easier lookup
        existing_sections = {section.id: section for section in instance.sections.all()}
        updated_sections = []

        for section_data in sections_data:
            section_id = section_data.get("id")
            fields_data = section_data.pop("form_fields", [])

            if section_id and section_id in existing_sections:
                section = existing_sections.pop(section_id)
                section.name = section_data.get("name", section.name)
                section.save()
            else:
                section = Section.objects.create(form=instance, **section_data)

            updated_sections.append(section)

            existing_fields = {field.id: field for field in section.form_fields.all()}
            updated_fields = []

            for field_data in fields_data:
                field_id = field_data.get("id")
                choices_data = field_data.pop("choices", [])

                if field_id and field_id in existing_fields:
                    field = existing_fields.pop(field_id)
                    field.label = field_data.get("label", field.label)
                    field.field_type = field_data.get("field_type", field.field_type)
                    field.is_required = field_data.get("is_required", field.is_required)
                    field.is_visible = field_data.get("is_visible", field.is_visible)
                    field.placeholder = field_data.get("placeholder", field.placeholder)
                    field.save()
                else:
                    field = Field.objects.create(section=section, **field_data)

                updated_fields.append(field)

                existing_choices = {choice.id: choice for choice in field.choices.all()}
                new_choices = []

                for choice_data in choices_data:
                    choice_id = choice_data.get("id")

                    if choice_id and choice_id in existing_choices:
                        choice = existing_choices.pop(choice_id)
                        choice.choice_text = choice_data.get("choice_text", choice.choice_text)
                        choice.save()
                    else:
                        choice = FieldChoice.objects.create(field=field, **choice_data)

                    new_choices.append(choice)

                field.choices.set(new_choices)

            for field in existing_fields.values():
                field.delete()

        for section in existing_sections.values():
            section.delete()

        return instance
