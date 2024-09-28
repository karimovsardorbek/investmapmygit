from rest_framework import serializers
from ..models.investor_company import InvestmentCompany, PortfolioCompany, Investment


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ['portfolio_company', 'stage', 'investment_type', 'amount', 'date']


class PortfolioCompanySerializer(serializers.ModelSerializer):
    investments = InvestmentSerializer(many=True, read_only=True)
    class Meta:
        model = PortfolioCompany
        fields = ['id', 'name', 'sector', 'location', 'date_founded', 'investments']


class InvestmentCompanyDetailSerializer(serializers.ModelSerializer):
    portfolio_companies = PortfolioCompanySerializer(many=True, read_only=True)

    class Meta:
        model = InvestmentCompany
        fields = ['id', 'company_name', 'description', 'website', 'logo', 'address', 
                  'date_founded', 'headquarters', 'total_investments', 
                  'number_of_exits', 'number_of_portfolio_organizations',
                  'total_portfolio_value', 'portfolio_companies', 'sectors',
                  'twitter_url', 'linkedin_url', 'facebook_url', 'created_at', 'updated_at']


class InvestmentStatisticsSerializer(serializers.ModelSerializer):
    total_investments = serializers.SerializerMethodField()
    investments_over_time = serializers.SerializerMethodField()
    investments_by_sector = serializers.SerializerMethodField()
    investments_by_location = serializers.SerializerMethodField()
    investments_by_stage = serializers.SerializerMethodField()

    class Meta:
        model = InvestmentCompany
        fields = [
            'company_name',
            'total_investments',
            'investments_over_time',
            'investments_by_sector',
            'investments_by_location',
            'investments_by_stage',
        ]

    def get_total_investments(self, obj):
        # Total investments the company has made
        return obj.investments.count()

    def get_investments_over_time(self, obj):
        # Group investments by year and return the count for each year
        investments = obj.investments.all()
        investment_years = {}
        for investment in investments:
            year = investment.date.year
            investment_years[year] = investment_years.get(year, 0) + 1
        return investment_years

    def get_investments_by_sector(self, obj):
        # Group investments by sector and calculate percentage
        investments = obj.investments.select_related('portfolio_company')
        sector_count = {}
        total_investments = investments.count()

        for investment in investments:
            sector = investment.portfolio_company.sector
            if sector:
                sector_count[sector] = sector_count.get(sector, 0) + 1

        sector_percentage = {k: (v / total_investments) * 100 for k, v in sector_count.items()}
        return sector_percentage

    def get_investments_by_location(self, obj):
        # Group investments by location and calculate percentage
        investments = obj.investments.select_related('portfolio_company')
        location_count = {}
        total_investments = investments.count()

        for investment in investments:
            location = investment.portfolio_company.location
            if location:
                location_count[location] = location_count.get(location, 0) + 1

        location_percentage = {k: (v / total_investments) * 100 for k, v in location_count.items()}
        return location_percentage

    def get_investments_by_stage(self, obj):
        # Group investments by stage and calculate percentage
        investments = obj.investments.all()
        stage_count = {}
        total_investments = investments.count()

        for investment in investments:
            stage = investment.stage
            stage_count[stage] = stage_count.get(stage, 0) + 1

        stage_percentage = {k: (v / total_investments) * 100 for k, v in stage_count.items()}
        return stage_percentage
