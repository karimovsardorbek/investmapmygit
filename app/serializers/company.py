from rest_framework import serializers
from ..models.company import Company


class CompanySerializer(serializers.ModelSerializer):
    date_of_registration = serializers.DateField(input_formats=['%m/%d/%Y'])  
    class Meta:
        model = Company
        # Exclude `created_by` since it will be set in the view or serializer
        exclude = ['created_by']

    def create(self, validated_data):
        # Add the `created_by` field to the validated data
        created_by = self.context['request'].user
        company = Company.objects.create(created_by=created_by, **validated_data)
        return company