from rest_framework import serializers
from django.utils.translation import get_language

from ..models.projects import (
    Project, 
    Founder, 
    PitchDeckSection,
    SubCategory, 
    Category,
)

from django.db.models import Sum
from ..models.investor import Investor, Check
from ..serializers.investor import InvestorSerializer


class SubCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')  # Get the name of the related Category

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category_name']


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)  # Nest SubCategorySerializer

    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategories']


# Step 2: Founder Information
class FounderSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(write_only=True)  # Add this line

    class Meta:
        model = Founder
        fields = ['id', 'name', 'role', 'email', 'phone_number', 'linkedin_profile', 'bio', 'project_id']

    def create(self, validated_data):
        # Retrieve the project instance using the project_id
        project_id = validated_data.pop('project_id')
        project = Project.objects.get(id=project_id)
        
        # Create the Founder instance with the project
        founder = Founder.objects.create(project=project, **validated_data)
        return founder

    def update(self, instance, validated_data):
        # Retrieve the project instance using the project_id if provided
        project_id = validated_data.pop('project_id', None)
        if project_id:
            instance.project = Project.objects.get(id=project_id)
        
        # Update the Founder instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PitchDeckSectionSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(write_only=True)
    sections = serializers.SerializerMethodField()  # This will include all sections under a single key

    class Meta:
        model = PitchDeckSection
        fields = [
            'id', 'sections', 'created_at', 'updated_at', 'project', 'project_id'
        ]

    def validate(self, data):
        project_id = data.get('project_id')
        if project_id is None:
            raise serializers.ValidationError({"project_id": "This field is required."})
        return data

    def create(self, validated_data):
        project_id = validated_data.pop('project_id')
        project = Project.objects.get(id=project_id)
        pitchdeck_section = PitchDeckSection.objects.create(project=project, **validated_data)
        return pitchdeck_section

    def update(self, instance, validated_data):
        project_id = validated_data.pop('project_id', None)
        if project_id:
            instance.project = Project.objects.get(id=project_id)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def get_language(self):
        # Use Django's built-in get_language() function
        return get_language() or 'en'
    
    # Consolidating all sections under 'sections'
    def get_sections(self, obj):
        lang = self.get_language()

        def get_field(instance, field_name):
            return getattr(instance, field_name, None) or getattr(instance, f"{field_name}_eng", None)

        return {
            'problem': {
                'name': get_field(obj, f'problem_name_{lang}'),
                'description': get_field(obj, f'problem_description_{lang}'),
                'image': obj.problem_image.url if obj.problem_image else None
            },
            'solution': {
                'name': get_field(obj, f'solution_name_{lang}'),
                'description': get_field(obj, f'solution_description_{lang}'),
                'image': obj.solution_image.url if obj.solution_image else None
            },
            'market_size': {
                'name': get_field(obj, f'market_size_name_{lang}'),
                'description': get_field(obj, f'market_size_description_{lang}'),
                'image': obj.market_size_image.url if obj.market_size_image else None
            },
            'target_customer': {
                'name': get_field(obj, f'target_customer_name_{lang}'),
                'description': get_field(obj, f'target_customer_description_{lang}'),
                'image': obj.target_customer_image.url if obj.target_customer_image else None
            },
            'how_it_works': {
                'name': get_field(obj, f'how_it_works_name_{lang}'),
                'description': get_field(obj, f'how_it_works_description_{lang}'),
                'image': obj.how_it_works_image.url if obj.how_it_works_image else None
            },
            'special_sauce': {
                'name': get_field(obj, f'special_sauce_name_{lang}'),
                'description': get_field(obj, f'special_sauce_description_{lang}'),
                'image': obj.special_sauce_image.url if obj.special_sauce_image else None
            },
            'team': {
                'name': get_field(obj, f'team_name_{lang}'),
                'description': get_field(obj, f'team_description_{lang}'),
                'image': obj.team_image.url if obj.team_image else None
            },
            'why_now': {
                'name': get_field(obj, f'why_now_name_{lang}'),
                'description': get_field(obj, f'why_now_description_{lang}'),
                'image': obj.why_now_image.url if obj.why_now_image else None
            },
            'business_model': {
                'name': get_field(obj, f'business_model_name_{lang}'),
                'description': get_field(obj, f'business_model_description_{lang}'),
                'image': obj.business_model_image.url if obj.business_model_image else None
            },
            'competitors': {
                'name': get_field(obj, f'competitors_name_{lang}'),
                'description': get_field(obj, f'competitors_description_{lang}'),
                'image': obj.competitors_image.url if obj.competitors_image else None
            },
            'tractions': {
                'name': get_field(obj, f'tractions_name_{lang}'),
                'description': get_field(obj, f'tractions_description_{lang}'),
                'image': obj.tractions_image.url if obj.tractions_image else None
            },
            'financial_acquisitions': {
                'name': get_field(obj, f'financial_acquisitions_name_{lang}'),
                'description': get_field(obj, f'financial_acquisitions_description_{lang}'),
                'image': obj.financial_acquisitions_image.url if obj.financial_acquisitions_image else None
            },
            'technology': {
                'name': get_field(obj, f'technology_name_{lang}'),
                'description': get_field(obj, f'technology_description_{lang}'),
                'image': obj.technology_image.url if obj.technology_image else None
            }
        }


class ProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['company']


class ProjectListSerializer(serializers.ModelSerializer):
    founders = FounderSerializer(many=True)
    pitchdeck_sections = PitchDeckSectionSerializer(many=True)
    sub_category_name = serializers.ReadOnlyField(source='sub_category.name')  # Get the subcategory name
    total_invested_amount = serializers.SerializerMethodField()
    percent_invested = serializers.SerializerMethodField()
    progress_bar = serializers.SerializerMethodField()
    start_date = serializers.SerializerMethodField()  # Use the application 'visible' date
    unique_investors_count = serializers.SerializerMethodField()  
    investors = serializers.SerializerMethodField() # New field to count unique investors

    class Meta:
        model = Project
        fields = ['id', 'startup_name', 'tagline', 'country', 'region', 'district', 'website_url', 
                  'linkedin', 'project_image', 'project_overview', 'elevator_pitch_video', 
                  'how_it_works_video', 'funding_goal', 'use_of_funds', 'business_plan', 
                  'financial_statements', 'other_documents', 'created_at', 'updated_at', 
                  'founders', 'pitchdeck_sections', 'sub_category_name', 'total_invested_amount', 
                  'percent_invested', 'progress_bar', 'start_date', 'time_limit', 'min_amount', 
                  'unique_investors_count', 'investors']  # Include unique_investors_count
        
    def get_total_invested_amount(self, obj):
        total_investment = Check.objects.filter(project=obj).aggregate(total=Sum('amount'))['total'] or 0
        return total_investment

    def get_percent_invested(self, obj):
        total_investment = self.get_total_invested_amount(obj)
        if obj.funding_goal > 0:
            return (total_investment / obj.funding_goal) * 100
        return 0

    def get_progress_bar(self, obj):
        return self.get_percent_invested(obj)

    def get_start_date(self, obj):
        application = obj.applications.filter(status='visible').order_by('last_updated').first()
        return application.last_updated if application else None

    # Method to get the number of unique investors
    def get_unique_investors_count(self, obj):
        unique_investors = obj.projects_investor.values('investor').distinct()
        return unique_investors.count()

    def get_investors(self, obj):
        # Get all investors who made a transaction on this project
        investors = Investor.objects.filter(investor_transaction__project=obj).distinct()
        return InvestorSerializer(investors, many=True).data


class ProjectListInvestorSerializer(serializers.ModelSerializer):
    sub_category_name = serializers.ReadOnlyField(source='sub_category.name')
    total_invested_amount = serializers.SerializerMethodField()
    percent_invested = serializers.SerializerMethodField()
    progress_bar = serializers.SerializerMethodField()
    me_invested = serializers.SerializerMethodField()
    start_date = serializers.SerializerMethodField()
    investor_equity = serializers.SerializerMethodField()
    
    # New fields
    equity_not_on_sale = serializers.SerializerMethodField()
    sum_investor_equity = serializers.SerializerMethodField()
    unsold_equity = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'startup_name', 'funding_goal', 'total_invested_amount', 'percent_invested', 
            'progress_bar', 'me_invested', 'start_date', 'time_limit', 'sub_category_name', 
            'investor_equity', 'equity_not_on_sale', 'sum_investor_equity', 'unsold_equity'
        ]

    def get_total_invested_amount(self, obj):
        """Calculate the total amount invested in the project using the Check model."""
        total_investment = Check.objects.filter(project=obj).aggregate(total=Sum('amount'))['total'] or 0
        return total_investment

    def get_percent_invested(self, obj):
        total_investment = self.get_total_invested_amount(obj)
        if obj.funding_goal > 0:
            return (total_investment / obj.funding_goal) * 100
        return 0

    def get_progress_bar(self, obj):
        return self.get_percent_invested(obj)

    def get_me_invested(self, obj):
        """Calculate the current user's investment in the project using the Check model."""
        user = self.context['request'].user
        if user.is_authenticated and hasattr(user, 'investor'):
            investor = user.investor
            my_investment = Check.objects.filter(project=obj, investor=investor).aggregate(total=Sum('amount'))['total'] or 0
            percent_invested = (my_investment / obj.funding_goal) * 100 if obj.funding_goal > 0 else 0
            return {
                'amount': my_investment,
                'percent': percent_invested
            }
        return {
            'amount': 0,
            'percent': 0
        }

    def get_start_date(self, obj):
        application = obj.applications.filter(status='visible').order_by('last_updated').first()
        if application:
            return application.last_updated
        return None
    
    def get_investor_equity(self, obj):
        """Fetch the equity the current investor has in the project."""
        user = self.context['request'].user
        if user.is_authenticated and hasattr(user, 'investor'):
            investor = user.investor
            investment = obj.investments.filter(investor=investor).first()
            if investment:
                return investment.equity
        return 0  # Return 0 if no investment found

    def get_equity_not_on_sale(self, obj):
        """Calculate project equity that is not on sale."""
        return 100 - obj.equity

    def get_sum_investor_equity(self, obj):
        """Calculate the sum of all investor equity in the project."""
        return obj.investments.aggregate(total=Sum('equity'))['total'] or 0

    def get_unsold_equity(self, obj):
        """Calculate the remaining unsold equity."""
        total_investor_equity = self.get_sum_investor_equity(obj)
        return obj.equity - total_investor_equity