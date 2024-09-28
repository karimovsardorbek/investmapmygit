from rest_framework import serializers

from ..models.bank_council import (
    BankMember, 
    BankCouncil, 
    Meeting, 
    Bank, 
    Position, 
)

from user.serializers import CustomUserSerializer
from .application import Application


class MeetingSerializer(serializers.ModelSerializer):
    selected_members = serializers.PrimaryKeyRelatedField(queryset=BankMember.objects.all(), many=True)
    selected_applications = serializers.PrimaryKeyRelatedField(queryset=Application.objects.all(), many=True)

    class Meta:
        model = Meeting
        fields = ['id', 'name', 'date', 'selected_members', 'selected_applications', 'status', 'created_by']


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ['id', 'name']


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'title']


class BankMemberSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    position = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all())
    
    class Meta:
        model = BankMember
        fields = ['user', 'position', 'created_by']
        read_only_fields = ['created_by']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        request = self.context.get('request')
        user = CustomUserSerializer.create(CustomUserSerializer(), validated_data=user_data)
        bank_member = BankMember.objects.create(user=user, created_by=request.user, **validated_data)
        return bank_member


class BankCouncilSerializer(serializers.ModelSerializer):
    members = BankMemberSerializer(many=True)

    class Meta:
        model = BankCouncil
        fields = ['id', 'name', 'members']