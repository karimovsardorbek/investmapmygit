from rest_framework import serializers
from ..models.moderator import Moderator
from ..models.application import Application

class ModeratorProfileSerializer(serializers.ModelSerializer):
    # Access fields of CustomUser through the 'user' relation
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    middle_name = serializers.CharField(source='user.middle_name', allow_null=True)
    birth_date = serializers.DateField(source='user.birth_date')
    gender = serializers.CharField(source='user.gender')
    email = serializers.EmailField(source='user.email')
    phone_number = serializers.CharField(source='user.phone_number')
    roles = serializers.StringRelatedField(source='user.roles', many=True)

    class Meta:
        model = Moderator
        fields = [
            'first_name', 'last_name', 'middle_name', 'birth_date', 'gender', 
            'email', 'phone_number', 'roles'
        ]


class ModeratorReviewSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Application.STATUS_CHOICES)
    comment = serializers.CharField(max_length=500, required=False)

    
class ModeratorUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    middle_name = serializers.CharField(source='user.middle_name', required=False)
    birth_date = serializers.DateField(source='user.birth_date', required=False)

    class Meta:
        model = Moderator
        fields = ['first_name', 'last_name', 'middle_name', 'birth_date']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()
        return instance