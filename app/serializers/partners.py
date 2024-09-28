from rest_framework import serializers
from ..models.partners import Partner


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['id', 'name', 'description_uz', 'description_ru', 'description_eng', 'logo', 'created_at', 'updated_at']
