from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from ..models.company import Company

from ..models.projects import (
    Project, 
    Founder, 
    PitchDeckSection, 
    Category,
)

from ..serializers.projects import ( 
    ProjectSerializer,
    FounderSerializer,
    PitchDeckSectionSerializer,
    ProjectListSerializer,
    CategorySerializer, 
)

from ..serializers.application import ApplicationSerializer
from ..models.application import Application
from django_filters import rest_framework as filters
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema


class CreateUpdateProjectView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ProjectSerializer)
    def post(self, request, *args, **kwargs):
        try:
            company = Company.objects.get(created_by=request.user)
        except Company.DoesNotExist:
            return Response({"error": "You do not have an associated company."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save(company=company)
            return Response({
                "message": "Project created successfully.",
                "project_id": str(project.id)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=ProjectSerializer)
    def put(self, request, *args, **kwargs):
        project_id = kwargs.get('id', None)

        try:
            company = Company.objects.get(created_by=request.user)
        except Company.DoesNotExist:
            return Response({"error": "You do not have an associated company."}, status=status.HTTP_400_BAD_REQUEST)

        if not project_id:
            return Response({"error": "Project ID is required for updating."}, status=status.HTTP_400_BAD_REQUEST)

        project = get_object_or_404(Project, id=project_id)

        if project.company != company:
            return Response({"error": "You do not have permission to update this project."}, status=status.HTTP_403_FORBIDDEN)


        data = request.data.copy()

        if 'time_limit' in data:
            try:
                entered_time_limit = int(data['time_limit'])
                data['time_limit'] = project.time_limit + entered_time_limit
            except ValueError:
                return Response({"error": "Invalid time limit provided."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProjectSerializer(project, data=data, partial=True)
        if serializer.is_valid():
            project = serializer.save()
            return Response({
                "message": "Project updated successfully.",
                "project_id": str(project.id)
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FounderCreateUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=FounderSerializer)
    def post(self, request, *args, **kwargs):
        serializer = FounderSerializer(data=request.data)
        
        if serializer.is_valid():
            founder = serializer.save()
            return Response({
                "message": "Founder created successfully.",
                "founder_id": str(founder.id)
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(request_body=FounderSerializer)
    def put(self, request, *args, **kwargs):
        founder_id = kwargs.get('id')
        try:
            founder = Founder.objects.get(id=founder_id)
        except Founder.DoesNotExist:
            return Response({"error": "Founder not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = FounderSerializer(founder, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Founder updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PitchDeckSectionCreateUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=PitchDeckSectionSerializer)
    def post(self, request, *args, **kwargs):
        serializer = PitchDeckSectionSerializer(data=request.data)
        
        if serializer.is_valid():
            pitchdeck_section = serializer.save()
            return Response({"message": "PitchDeckSection created successfully.", "pitchdeck_section_id": pitchdeck_section.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=PitchDeckSectionSerializer)
    def put(self, request, *args, **kwargs):
        pitchdeck_id = kwargs.get('id')
        try:
            pitchdeck_section = PitchDeckSection.objects.get(id=pitchdeck_id)
        except PitchDeckSection.DoesNotExist:
            return Response({"error": "PitchDeckSection not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PitchDeckSectionSerializer(pitchdeck_section, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "PitchDeckSection updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProjectsPublicView(ListAPIView):
    serializer_class = ProjectListSerializer
    permission_classes = [AllowAny] 

    def get_queryset(self):
        return Project.objects.filter(applications__status='visible').distinct()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request 
        return context


class ProjectDetailView(RetrieveAPIView):
    queryset = Project.objects.filter(applications__status='visible').distinct()  
    serializer_class = ProjectListSerializer  
    permission_classes = [AllowAny]  
    lookup_field = 'id' 

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request 
        return context


class ProjectFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='sub_category__category__name', lookup_expr='icontains')  # Adjust field name
    funding_goal = filters.RangeFilter(field_name='funding_goal')

    class Meta:
        model = Project
        fields = ['category', 'funding_goal']


class ProjectSearchListView(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    filter_backends = [filters.DjangoFilterBackend, SearchFilter]  
    filterset_class = ProjectFilter  
    search_fields = ['sub_category__category__name', 'startup_name', 'tagline', 'funding_goal']  # Corrected field path
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Project.objects.filter(applications__status='visible').distinct()  # Apply additional filter for visible applications


class CategoryListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProjectApplicationsListView(ListAPIView):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')  
        return Application.objects.filter(project__id=project_id)