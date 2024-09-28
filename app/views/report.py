from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.db.models import Q
from ..models.report import Report
from ..serializers.report import ReportSerializer
from rest_framework.pagination import PageNumberPagination


class ReportPagination(PageNumberPagination):
    page_size = 9  # Set the number of reports per page
    page_size_query_param = 'page_size'  # Optional: Allow the client to change page size
    max_page_size = 100  # Optional: Set a maximum page size

class ReportListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        language = request.query_params.get('language', 'en')  # Default to English
        category = request.query_params.get('category')  # Optional category filter
        industry = request.query_params.get('industry')  # Optional industry filter
        report_type = request.query_params.get('report_type')  # Optional report type filter
        publish_year = request.query_params.get('year')  # Optional year filter
        search_query = request.query_params.get('search')  # Search query for title and description
        
        reports = Report.objects.all()

        # Filter by multiple categories if provided
        if category:
            category_list = category.split(',')  # Split by comma to allow multiple categories
            reports = reports.filter(category__in=category_list)
        
        # Filter by multiple industries if provided
        if industry:
            industry_list = industry.split(',')  # Split by comma to allow multiple industries
            reports = reports.filter(industry__in=industry_list)
        
        # Filter by multiple report types if provided
        if report_type:
            report_type_list = report_type.split(',')  # Split by comma to allow multiple report types
            reports = reports.filter(report_type__in=report_type_list)

        # Filter by publishing year if provided
        if publish_year:
            reports = reports.filter(publish_date__year=publish_year)

        # Search by title and description based on the language
        if search_query:
            reports = reports.filter(
                Q(title_uz__icontains=search_query) |
                Q(description_uz__icontains=search_query) |
                Q(title_ru__icontains=search_query) |
                Q(description_ru__icontains=search_query) |
                Q(title_en__icontains=search_query) |
                Q(description_en__icontains=search_query)
            ).distinct()

        # Apply pagination
        paginator = ReportPagination()
        paginated_reports = paginator.paginate_queryset(reports, request)

        # Serialize the paginated data
        serializer = ReportSerializer(paginated_reports, many=True, context={'language': language, 'request': request})

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)