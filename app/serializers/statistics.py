from rest_framework import serializers
from ..models.statistics import Statistics


class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = [
            'id',
            'investor_count',
            'project_count',
            'description_uz',
            'description_ru',
            'description_eng',
            'value'
        ]