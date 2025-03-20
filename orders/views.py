from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order
from .serializers import OrderSerializer
from form.models import Form
import logging
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from rest_framework.pagination import PageNumberPagination

logger = logging.getLogger(__name__)  # Use logging instead of print

class OrderView(APIView):
    def get(self, request, *args, **kwargs):
        """List all orders"""
        orders = Order.objects.all().order_by("-submitted_at")  # Show latest orders first
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """Submit an order (Form submission)"""

        logger.info("Incoming request data: %s", request.data)  # Log instead of print

        form_id = request.data.get("form_id")
        field_values = request.data.get("field_values", {})

        if not form_id:
            return Response({"error": "Form ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(field_values, dict):
            return Response({"error": "Invalid field_values format."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            form = Form.objects.get(id=form_id)
        except Form.DoesNotExist:
            return Response({"error": "Form not found."}, status=status.HTTP_404_NOT_FOUND)

        order = Order.objects.create(
            form=form,
            field_values=field_values if field_values else {}
        )

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveUpdateAPIView):  
    """Retrieve or update an order's status"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer



class OrderPagination(PageNumberPagination):
    page_size = 10  # Default number of items per page
    page_size_query_param = "page_size"
    max_page_size = 30  # Prevent excessive load






