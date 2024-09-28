from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from ..models.testimonials import Testimonial
from ..serializers.testimonials import TestimonialSerializer
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema


class TestimonialListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        testimonials = Testimonial.objects.all()
        serializer = TestimonialSerializer(testimonials, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class TestimonialCreateView(APIView):
    permission_classes = [IsAdminUser]  
    @swagger_auto_schema(request_body=TestimonialSerializer)

    def post(self, request, *args, **kwargs):
        serializer = TestimonialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TestimonialUpdateView(APIView):
    permission_classes = [IsAdminUser] 
    @swagger_auto_schema(request_body=TestimonialSerializer)
    def put(self, request, pk, *args, **kwargs):
        testimonial = get_object_or_404(Testimonial, pk=pk)
        serializer = TestimonialSerializer(testimonial, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TestimonialDeleteView(APIView):
    permission_classes = [IsAdminUser] 

    def delete(self, request, pk, *args, **kwargs):
        testimonial = get_object_or_404(Testimonial, pk=pk)
        testimonial.delete()
        return Response({"message": "Testimonial deleted successfully."}, status=status.HTTP_200_OK)