from rest_framework import generics
from ..models.company_info import CompanyInfo
from ..serializers.company_info import CompanyListSerializer, CompanyInfoSerializer
import django_filters
from ..models.company_info import CompanyInfo
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny


class CompanyInfoFilter(django_filters.FilterSet):
    # Search by keyword
    keyword = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    # Filter by founding year (range)
    founding_year_from = django_filters.NumberFilter(field_name='founded_year', lookup_expr='gte')
    founding_year_to = django_filters.NumberFilter(field_name='founded_year', lookup_expr='lte')

    # Multiple sectors filter
    sector = django_filters.CharFilter(method='filter_by_sector')

    # Multiple headquarters cities filter
    headquarters = django_filters.CharFilter(method='filter_by_headquarters')

    # Multiple funding types filter
    funding_type = django_filters.CharFilter(method='filter_by_funding_type')

    # Single funding stage filter (no need for custom method)
    last_funding_stage = django_filters.CharFilter(field_name='funding_rounds__last_funding_stage', lookup_expr='icontains')

    class Meta:
        model = CompanyInfo
        fields = ['keyword', 'founding_year_from', 'founding_year_to', 'sector', 'headquarters',
                  'funding_type', 'last_funding_stage']

    # Custom method to filter by sector
    def filter_by_sector(self, queryset, name, value):
        sectors = value.split(',')  # Split the incoming value by comma
        return queryset.filter(sector__in=sectors).distinct()

    # Custom method to filter by headquarters
    def filter_by_headquarters(self, queryset, name, value):
        cities = value.split(',')
        return queryset.filter(headquarters__in=cities).distinct()

    # Custom method to filter by funding type
    def filter_by_funding_type(self, queryset, name, value):
        funding_types = value.split(',')  # Split the incoming value by comma
        return queryset.filter(funding_rounds__round_type__in=funding_types).distinct()


class CompanyInfoListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompanyInfoFilter


class CompanyInfoDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer
    lookup_field = 'id'  # You can also use 'pk' by default