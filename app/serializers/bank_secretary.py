from rest_framework import serializers
from ..models.bank_secretary import BankSecretary
from user.serializers import CustomUserSerializer


class BankSecretaryProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = BankSecretary
        fields = ['user', 'bank']

    def update(self, instance, validated_data):
        # Update the user details if 'user' is in validated_data
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = CustomUserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()

        # Update the BankSecretary details
        instance.bank = validated_data.get('bank', instance.bank)
        instance.save()
        return instance