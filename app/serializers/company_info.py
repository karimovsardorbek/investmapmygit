from rest_framework import serializers

from ..models.company_info import (
    CompanyInfo, 
    Funding,
    Acquisition,
    CompanyInvestment,
    Financials,
    Story,
)


class FundingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funding
        fields = ['amount_raised', 'currency', 'round_type', 'number_of_investors', 'announced_date', 'last_funding_stage']
        

class CompanyInfoInvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInvestment
        fields = ['portfolio_company', 'sector', 'stage', 'amount_invested', 'date_announced']


class AcquisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acquisition
        fields = ['acquired_company', 'sector', 'acquisition_date', 'acquisition_price']


class FinancialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Financials
        fields = [
            'year', 'total_revenue', 'total_expenses', 'profit_before_tax', 'profit_after_tax',
            'total_assets', 'total_liabilities', 'equity_share_capital', 'current_liabilities',
            'non_current_liabilities', 'cash_flow_operating', 'cash_flow_investing',
            'cash_flow_financing', 'cash_balance', 'net_profit_margin', 'return_on_assets',
            'current_ratio', 'debt_equity_ratio'
        ]


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['title', 'author', 'date_published', 'url']


class CompanyInfoSerializer(serializers.ModelSerializer):
    funding_rounds = FundingSerializer(many=True)
    investments = CompanyInfoInvestmentSerializer(many=True)
    acquisitions = AcquisitionSerializer(many=True)
    financials = FinancialsSerializer(many=True)
    stories = StorySerializer(many=True)

    class Meta:
        model = CompanyInfo
        fields = ['id', 'name', 'sector', 'founded_year', 'headquarters', 'founders',
                  'funding_rounds', 'investments', 'acquisitions', 'financials', 'stories',
                  'country', 'state', 'number_of_investors', 'amount_raised',
                  'amount_raised_currency', 'company_type', 'last_funding_type', 
                  'last_funding_stage', 'ipo_status', 'number_of_employees',
                  'website', 'facebook_url', 'linkedin_url', 'twitter_url']


class CompanyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyInfo
        fields = ['id', 'name', 'sector', 'founded_year', 'headquarters', 'founders',
                  'country', 'state', 'number_of_investors', 'amount_raised',
                  'amount_raised_currency', 'company_type', 'last_funding_type', 
                  'last_funding_stage', 'ipo_status', 'number_of_employees',
                  'website', 'facebook_url', 'linkedin_url', 'twitter_url']