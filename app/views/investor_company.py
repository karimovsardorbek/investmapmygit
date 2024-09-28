from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.investor_company import InvestmentCompany, Investment
from ..serializers.investor_company import InvestmentCompanyDetailSerializer, InvestmentStatisticsSerializer
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from django_filters import rest_framework as filters


class InvestmentCompanyListView(APIView):
    permission_classes = [AllowAny]  # No authentication required for GET requests

    def get_object(self, pk=None):
        if pk:
            try:
                return InvestmentCompany.objects.get(pk=pk)
            except InvestmentCompany.DoesNotExist:
                raise Http404
        return InvestmentCompany.objects.all()

    def get(self, request, pk=None):
        # If pk is provided, return a single company
        if pk:
            investment_company = self.get_object(pk)
            serializer = InvestmentCompanyDetailSerializer(investment_company)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Otherwise, filter the list of companies
        investment_companies = self.get_object()  # Get all companies

        # Apply filtering
        filterset = InvestmentCompanyFilter(request.GET, queryset=investment_companies)
        
        if not filterset.is_valid():
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)

        filtered_companies = filterset.qs
        serializer = InvestmentCompanyDetailSerializer(filtered_companies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InvestmentCompanyUpdateView(APIView):
    permission_classes = [IsAuthenticated]  # Authentication required for PUT requests

    def get_object(self, pk):
        try:
            return InvestmentCompany.objects.get(pk=pk)
        except InvestmentCompany.DoesNotExist:
            raise Http404

    @swagger_auto_schema(request_body=InvestmentCompanyDetailSerializer)
    def put(self, request, pk):
        # Update the investment company details if authorized
        investment_company = self.get_object(pk)
        if request.user.has_perm('app.change_investmentcompany'):  # Check for appropriate permissions
            serializer = InvestmentCompanyDetailSerializer(investment_company, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Not authorized to update this data'}, status=status.HTTP_403_FORBIDDEN)


class InvestmentStatisticsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            investment_company = InvestmentCompany.objects.get(pk=pk)
        except InvestmentCompany.DoesNotExist:
            return Response({"error": "Investment Company not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = InvestmentStatisticsSerializer(investment_company)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class InvestmentCompanyFilter(filters.FilterSet):
    # Search by keyword (company name or description)
    keyword = filters.CharFilter(field_name='company_name', lookup_expr='icontains')

    # Filter by investor type
    investor_type = filters.CharFilter(method='filter_by_investor_type')

    # Filter by number of investments
    min_investments = filters.NumberFilter(field_name='total_investments', lookup_expr='gte')
    max_investments = filters.NumberFilter(field_name='total_investments', lookup_expr='lte')

    # Filter by number of exits
    min_exits = filters.NumberFilter(field_name='number_of_exits', lookup_expr='gte')
    max_exits = filters.NumberFilter(field_name='number_of_exits', lookup_expr='lte')

    # Filter by number of portfolio organizations
    min_portfolio_orgs = filters.NumberFilter(field_name='number_of_portfolio_organizations', lookup_expr='gte')
    max_portfolio_orgs = filters.NumberFilter(field_name='number_of_portfolio_organizations', lookup_expr='lte')

    # Filter by sector
    sector = filters.CharFilter(method='filter_by_sector')

    # Filter by investment type (comma-separated values)
    investment_type = filters.CharFilter(method='filter_by_investment_type')

    # Filter by investment stage (using ChoiceFilter)
    investment_stage = filters.ChoiceFilter(
        field_name='investments__stage',
        choices=Investment.STAGE_CHOICES
    )

    # Filter by portfolio company name (invested in)
    invested_in = filters.CharFilter(method='filter_by_portfolio_company')

    class Meta:
        model = InvestmentCompany
        fields = ['keyword', 'investor_type', 'min_investments', 'max_investments', 'min_exits', 'max_exits',
                  'min_portfolio_orgs', 'max_portfolio_orgs', 'sector', 'investment_stage', 'investment_type', 'invested_in']

    def filter_by_investor_type(self, queryset, name, value):
        # Split the incoming investor types by comma
        investor_types = value.split(',')
        # Filter by matching any of the provided investor types
        return queryset.filter(sectors__icontains=value) 

    def filter_by_portfolio_company(self, queryset, name, value):
        # Filter investment companies that have invested in a portfolio company with the given name
        return queryset.filter(portfolio_companies__name__icontains=value).distinct()

    def filter_by_investment_type(self, queryset, name, value):
        # Split the incoming investment types by comma and filter by any of them
        investment_types = value.split(',')
        return queryset.filter(investments__investment_type__in=investment_types).distinct()

    def filter_by_sector(self, queryset, name, value):
        # Split the incoming sectors by comma and filter by any of them
        sectors = value.split(',')
        return queryset.filter(sectors__in=sectors).distinct()