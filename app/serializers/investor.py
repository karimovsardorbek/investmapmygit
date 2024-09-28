from rest_framework import serializers

from ..models.investor import (
    Card, 
    BankAccountInfo, 
    InvestorDocument, 
    Transaction, 
    Investor,
)

from user.serializers import UserSimpleProfileSerializer
from app.serializers.payment import InvoiceSerializer
from app.models.investor import Check
from app.models.club import Club
from django.db.models import Sum


class BankCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'


class BankAccountInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccountInfo
        fields = '__all__'


class InvestorDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorDocument
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    invoice = InvoiceSerializer(read_only=True)  

    class Meta:
        model = Transaction
        fields = ['id', 'date', 'project_name', 'invoice', 'amount', 'card_number']


class InvestorSerializer(serializers.ModelSerializer):
    user = UserSimpleProfileSerializer(read_only=True)
    class Meta:
        model = Investor
        fields = ['id', 'user', 'investor_type']
        read_only_fields = ['investor_type']  # The investor_type should be read-only for non-admins


class InvesterUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    middle_name = serializers.CharField(source='user.middle_name', required=False)
    birth_date = serializers.DateField(source='user.birth_date', required=False)

    class Meta:
        model = Investor
        fields = ['first_name', 'last_name', 'middle_name', 'birth_date']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()
        return instance


class InvestorProfileSerializer(serializers.ModelSerializer):
    # Access fields of CustomUser through the 'user' relation
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    middle_name = serializers.CharField(source='user.middle_name', allow_null=True)
    birth_date = serializers.DateField(source='user.birth_date')
    gender = serializers.CharField(source='user.gender')
    email = serializers.EmailField(source='user.email')
    phone_number = serializers.CharField(source='user.phone_number')
    region = serializers.CharField(source='user.region')
    caunty = serializers.CharField(source='user.caunty')
    avatar = serializers.CharField(source='user.avatar')
    total_invested_amount = serializers.SerializerMethodField()
    average = serializers.SerializerMethodField()
    clubs = serializers.SerializerMethodField()
    number_of_invested = serializers.SerializerMethodField()

    class Meta:
        model = Investor
        fields = [
            'first_name', 'last_name', 'middle_name', 'birth_date', 'gender', 
            'email', 'phone_number','region','caunty','avatar','linkedin','total_invested_amount','average','clubs','number_of_invested'
        ]

    def get_total_invested_amount(self, obj):
        total_investment = Check.objects.filter(investor=obj).aggregate(total=Sum('amount'))['total'] or 0
        return total_investment

    def get_average(self,obj):
        total_investment = Check.objects.filter(investor=obj).aggregate(total=Sum('amount'))['total'] or 0
        count = Check.objects.filter(investor=obj).count()
        if not count or count == 0:
            count = 1
        return total_investment/count
    
    def get_clubs(self, obj):
        total_clubs = Club.objects.filter(members=obj).count()
        return total_clubs 

    def get_number_of_investments(self,obj):
        return Check.objects.filter(investor=obj).count()