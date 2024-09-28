from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.statistics import Statistics
from ..serializers.statistics import StatisticsSerializer
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from ..models.projects import Project
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema


class StatisticsView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny] 
        return super(StatisticsView, self).get_permissions()

    def update_counts(self, stats):
        stats.investor_count = get_user_model().objects.filter(roles__name='investor').count()
        stats.project_count = Project.objects.count()
        stats.save()

    def get(self, request, *args, **kwargs):
        language = request.headers.get('Accept-Language', 'uz').lower()
        stats = Statistics.objects.all()

        if not stats.exists():
            return Response({"error": "Statistics not found"}, status=status.HTTP_404_NOT_FOUND)

        for stat in stats:
            self.update_counts(stat)  

        serialized_data = []
        for stat in stats:
            if language == 'eng':
                description = stat.description_eng
            elif language == 'ru':
                description = stat.description_ru
            else: 
                description = stat.description_uz

            serialized_data.append({
                'id': stat.id,
                'investor_count': stat.investor_count,
                'project_count': stat.project_count,
                'description': description,
                'value': stat.value,
            })

        return Response(serialized_data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=StatisticsSerializer)
    def post(self, request, *args, **kwargs):
        serializer = StatisticsSerializer(data=request.data)
        if serializer.is_valid():
            stats = serializer.save()
            self.update_counts(stats)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatisticsUpdateView(APIView):
    permission_classes = [IsAdminUser]  

    def update_counts(self, stats):
        stats.investor_count = get_user_model().objects.filter(roles__name='investor').count()
        stats.project_count = Project.objects.count()
        stats.save()
        
    @swagger_auto_schema(request_body=StatisticsSerializer)
    def put(self, request, pk, *args, **kwargs):
        stats = get_object_or_404(Statistics, pk=pk)
        serializer = StatisticsSerializer(stats, data=request.data, partial=True)
        if serializer.is_valid():
            updated_stats = serializer.save()
            self.update_counts(updated_stats)  
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatisticsDeleteView(APIView):
    permission_classes = [IsAdminUser]  

    def update_counts_for_all(self):
        stats = Statistics.objects.all()
        for stat in stats:
            stat.investor_count = get_user_model().objects.filter(roles__name='investor').count()
            stat.project_count = Project.objects.count()
            stat.save()

    def delete(self, request, pk, *args, **kwargs):
        stats = get_object_or_404(Statistics, pk=pk)
        stats.delete()
        self.update_counts_for_all() 
        return Response({"message": "Statistics record deleted successfully."}, status=status.HTTP_200_OK)