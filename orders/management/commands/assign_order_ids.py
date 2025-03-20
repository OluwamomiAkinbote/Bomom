import uuid
from django.core.management.base import BaseCommand
from orders.models import Order

class Command(BaseCommand):
    help = "Assign unique numeric IDs to existing Orders without one."

    def handle(self, *args, **kwargs):
        orders_without_id = Order.objects.filter(unique_id__isnull=True)  # Get orders without a unique_id

        if not orders_without_id.exists():
            self.stdout.write(self.style.SUCCESS("All orders already have unique IDs."))
            return

        updated_count = 0

        for order in orders_without_id:
            unique_numeric_id = str(int(uuid.uuid4().int))[:7]  # Generate a 7-digit numeric ID

            # Ensure uniqueness by checking existing IDs
            while Order.objects.filter(unique_id=unique_numeric_id).exists():
                unique_numeric_id = str(int(uuid.uuid4().int))[:7]

            order.unique_id = unique_numeric_id
            order.save()
            updated_count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully assigned unique IDs to {updated_count} orders."))
2