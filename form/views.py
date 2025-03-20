from django.shortcuts import render
from rest_framework import generics
from .models import Form
from .serializers import FormSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404



class FormDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Form.objects.all()
    serializer_class = FormSerializer

    def get_object(self):
        unique_id = self.kwargs.get("unique_id")
        try:
            return Form.objects.get(unique_id=unique_id)
        except Form.DoesNotExist:
            raise NotFound({"error": "Form not found"})


class FormList(generics.ListCreateAPIView):
    queryset = Form.objects.all()
    serializer_class = FormSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)  # Debugging line
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)







class FormDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    lookup_field = "unique_id"  # ✅ Tell Django to use unique_id instead of pk

    def get_object(self):
        unique_id = self.kwargs.get("unique_id")
        print(f"Looking for Form with unique_id: {unique_id}")  # Debugging line

        form = get_object_or_404(Form, unique_id=unique_id)
        print(f"Found Form: {form}")  # Debugging line

        return form

