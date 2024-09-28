from rest_framework import serializers
from .models import CustomUser
from django.core.validators import validate_email

    
class UserLoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        identifier = data.get('identifier', '')
        password = data.get('password', '')

        user = None
        errors = {}

        if '@' in identifier:
            user = CustomUser.objects.filter(email__iexact=identifier).first()
            if not user:
                errors['email'] = "No user found with this email address."
        else:
            user = CustomUser.objects.filter(phone_number=identifier).first()
            if not user:
                errors['phone_number'] = "No user found with this phone number."

        if user:
            if not user.check_password(password):
                errors['password'] = "Incorrect password."
            if not user.is_active:
                errors['account'] = "This account is inactive."

        if errors:
            raise serializers.ValidationError(errors)

        return {'user': user}


class UserProfileSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'middle_name', 'birth_date', 'gender', 
            'email', 'phone_number', 'is_active', 'roles', 'company'
        ]


class UserSimpleProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'phone_number'
        ]


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'middle_name', 'birth_date', 'gender', 
            'email', 'phone_number', 'password'
        ]
        
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)  # Hash the password before saving
        user.save()
        return user