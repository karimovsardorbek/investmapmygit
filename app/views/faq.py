from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from django.shortcuts import get_object_or_404
from ..models.faq import FAQ
from ..serializers.faq import FAQSerializer, RaisingContactSerializer
from drf_yasg.utils import swagger_auto_schema


class FAQListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        language = request.headers.get('Accept-Language', 'uz').lower()

        faqs = FAQ.objects.all()

        if language == 'uz':
            serialized_data = [
                {
                    'id': item.id,
                    'question': item.question_uz,
                    'answer': item.answer_uz,
                    'created_at': item.created_at,
                    'updated_at': item.updated_at,
                } for item in faqs
            ]
        elif language == 'ru':
            serialized_data = [
                {
                    'id': item.id,
                    'question': item.question_ru,
                    'answer': item.answer_ru,
                    'created_at': item.created_at,
                    'updated_at': item.updated_at,
                } for item in faqs
            ]
        else: 
            serialized_data = [
                {
                    'id': item.id,
                    'question': item.question_eng,
                    'answer': item.answer_eng,
                    'created_at': item.created_at,
                    'updated_at': item.updated_at,
                } for item in faqs
            ]

        return Response(serialized_data, status=status.HTTP_200_OK)


class FAQCreateUpdateDeleteView(APIView):
    permission_classes = [IsAdminUser]  
    
    @swagger_auto_schema(request_body=FAQSerializer)
    def post(self, request, *args, **kwargs):
        serializer = FAQSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=FAQSerializer)
    def put(self, request, pk, *args, **kwargs):
        faq = get_object_or_404(FAQ, pk=pk)
        serializer = FAQSerializer(faq, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, *args, **kwargs):
        faq = get_object_or_404(FAQ, pk=pk)
        faq.delete()
        return Response({"message": "FAQ deleted successfully."}, status=status.HTTP_200_OK)


class RaisingContactCreateView(APIView):
    permission_classes = [AllowAny]  
    
    @swagger_auto_schema(request_body=RaisingContactSerializer)
    def post(self, request, *args, **kwargs):
        serializer = RaisingContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)