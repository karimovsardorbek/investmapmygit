from rest_framework import serializers
from ..models.application import (
    Application, 
    ApplicationScore, 
    ApplicationNotification
)
from ..models.bank_council import Criteria


class ApplicationSerializer(serializers.ModelSerializer):
    submission_date = serializers.DateTimeField(format="%m/%d/%Y") 
    last_updated = serializers.DateTimeField(format="%m/%d/%Y") 

    class Meta:
        model = Application
        fields = ['id', 'project', 'status', 'submission_date', 'last_updated', 'current_checker']
        read_only_fields = ['submission_date', 'last_updated', 'current_checker']


class ApplicationListSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.startup_name')
    submission_date = serializers.DateTimeField(format="%m/%d/%Y")
    last_updated = serializers.DateTimeField(format="%m/%d/%Y") 

    class Meta:
        model = Application
        fields = ['id', 'project_name', 'status', 'submission_date']


class ApplicationDetailSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.startup_name')
    owner_first_name = serializers.CharField(source='project.company.created_by.first_name')
    owner_last_name = serializers.CharField(source='project.company.created_by.last_name')
    owner_middle_name = serializers.CharField(source='project.company.created_by.middle_name')
    company_name = serializers.CharField(source='project.company.legal_name')

    class Meta:
        model = Application
        fields = [
            'id', 
            'project_name', 
            'owner_first_name', 
            'owner_last_name', 
            'owner_middle_name', 
            'company_name', 
            'status'
        ]


class ApplicationScoreSerializer(serializers.ModelSerializer):
    criteria_score = serializers.PrimaryKeyRelatedField(queryset=Criteria.objects.all(), write_only=True)
    member_name = serializers.CharField(source='member.user.get_full_name', read_only=True)
    score = serializers.DecimalField(max_digits=5, decimal_places=2)
    comment = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = ApplicationScore
        fields = ['criteria_score', 'score', 'comment', 'member_name']


class ApplicationNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationNotification
        fields = ['application', 'project_name', 'company_owner_first_name', 'company_owner_last_name', 'created_at']