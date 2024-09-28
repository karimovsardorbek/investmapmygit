from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..serializers.company import CompanySerializer
from ..models.company import Company
from drf_yasg.utils import swagger_auto_schema


class CreateCompanyView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CompanySerializer)
    def post(self, request, *args, **kwargs):
        serializer = CompanySerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            company = serializer.save()
            return Response({"message": "Company created successfully.", "company_id": str(company.id)}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CompanyUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CompanySerializer)
    def put(self, request, pk, *args, **kwargs):
        company = get_object_or_404(Company, pk=pk, created_by=request.user)

        serializer = CompanySerializer(company, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class UserCompanyDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        company = get_object_or_404(Company, created_by=request.user)

        serializer = CompanySerializer(company)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class CompanyListView(APIView):
    permission_classes = [AllowAny]  

    def get(self, request, *args, **kwargs):
        companies = Company.objects.all()

        serializer = CompanySerializer(companies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)