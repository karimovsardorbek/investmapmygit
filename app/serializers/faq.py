from rest_framework import serializers
from ..models.faq import FAQ, RaisingContact


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = [
            'id', 
            'question_uz', 'question_ru', 'question_eng', 
            'answer_uz', 'answer_ru', 'answer_eng', 
            'created_at', 'updated_at'
        ]


class RaisingContactSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=15)
    project_name = serializers.CharField(max_length=200) 
       
    class Meta:
        model = RaisingContact
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 'project_name'
        ]

    def create(self, validated_data):
        # Assuming RaisingContact is a Django model
        return RaisingContact.objects.create(**validated_data)