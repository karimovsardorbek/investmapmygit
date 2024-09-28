from rest_framework import serializers
from ..models.contact import ContactDetails, SendQuestion


class ContactDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactDetails
        fields = ['id', 'email1', 'email2', 'phone_number1', 'phone_number2', 'office_address', 'created_at', 'updated_at']


class SendQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendQuestion
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'message']