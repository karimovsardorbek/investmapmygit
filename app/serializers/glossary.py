from rest_framework import serializers
from ..models.glossary import Glossary, GlossarySection


class GlossarySectionSerializer(serializers.ModelSerializer):
    glossary_id = serializers.PrimaryKeyRelatedField(queryset=Glossary.objects.all(), source='glossary')
    image = serializers.ImageField()  # Include the section image

    class Meta:
        model = GlossarySection
        fields = ['id', 'glossary_id', 'name_uz', 'description_uz', 'name_ru', 'description_ru', 'name_en', 'description_en', 'image']  # Include the image field

class GlossarySerializer(serializers.ModelSerializer):
    sections = GlossarySectionSerializer(many=True, read_only=True)
    image = serializers.ImageField()  # Include the glossary image

    class Meta:
        model = Glossary
        fields = ['id', 'name_uz', 'description_uz', 'name_ru', 'description_ru', 'name_en', 'description_en', 'image', 'category', 'sections']  # Include the image field
