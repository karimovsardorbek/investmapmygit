from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from ..models.partners import Partner
from ..serializers.partners import PartnerSerializer
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema


class PartnerListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        language = request.headers.get('Accept-Language', 'eng').lower()

        partners = Partner.objects.all()

        serialized_data = []
        for partner in partners:
            if language == 'uz':
                description = partner.description_uz
            elif language == 'ru':
                description = partner.description_ru
            else:  
                description = partner.description_eng

            serialized_data.append({
                'id': partner.id,
                'name': partner.name,
                'description': description,
                'logo': partner.logo.url if partner.logo else None,
                'created_at': partner.created_at,
                'updated_at': partner.updated_at,
            })

        return Response(serialized_data, status=status.HTTP_200_OK)


class PartnerCreateView(APIView):
    permission_classes = [IsAdminUser]
    
    @swagger_auto_schema(request_body=PartnerSerializer)
    def post(self, request, *args, **kwargs):
        serializer = PartnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PartnerUpdateView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(request_body=PartnerSerializer)
    def put(self, request, pk, *args, **kwargs):
        partner = get_object_or_404(Partner, pk=pk)
        serializer = PartnerSerializer(partner, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PartnerDeleteView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk, *args, **kwargs):
        partner = get_object_or_404(Partner, pk=pk)
        partner.delete()
        return Response({"message": "Partner deleted successfully."}, status=status.HTTP_200_OK)