from rest_framework import serializers

from app.models.club import (
    Club,
    InvestorTransactionClub,
    ClubCheck,ClubBankAccountInfo,
    ClubInvoice,
    RequesteToJoinClub,
    )

from app.serializers.investor import InvestorSerializer


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = "__all__"

    def create(self, validated_data):
        user = self.context['request'].user.investor
        validated_data['investor'] = user  # Set the investor field
        return super().create(validated_data)


class ClubUpdateSerializer(serializers.ModelSerializer):
    logo = serializers.FileField(required=False)
    type = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    name = serializers.CharField(required =False)

    class Meta:
        model = Club
        fields = ['logo', 'type', 'description', 'min_amount','max_amount','percentage','fixed_price','name']

    def update(self, instance, validated_data):

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class ClubBankAccountSerialializer(serializers.ModelSerializer):
    class Meta:
        model = ClubBankAccountInfo
        fields = (
            'id',
            'bank_name',
            'account_number',
            'account_holder_name',
            'amount',
            'routing_number'
        )


class ClubGetSerializer(serializers.ModelSerializer):
    investor = InvestorSerializer()
    members = InvestorSerializer(many=True)  # Serialize many-to-many members

    financial_statement = serializers.SerializerMethodField(allow_null=True)
    class Meta:
        model = Club
        fields = (
            'id',
            'logo',
            'type',
            'investor',
            'description',
            'min_amount',
            'max_amount',
            'percentage',
            'fixed_price',
            'members',
            'name',
            'financial_statement'
        )

    def get_financial_statement(self,obj):
        bank_info = ClubBankAccountInfo.objects.filter(club = obj)
        return ClubBankAccountSerialializer(bank_info,many = True).data()


class ClubNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('id','name')


class RequestJoingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequesteToJoinClub
        fields = "__all__"


class RequestJoinCreateSerializer(serializers.Serializer):
    club_id = serializers.IntegerField()


class ApproveClubSerializer(serializers.Serializer):
    club_id = serializers.IntegerField()
    status = serializers.CharField()


class RequestJoinUpdateSerializer(serializers.Serializer):
    club_id = serializers.IntegerField()
    request_id = serializers.IntegerField()
    status = serializers.CharField()


class PaymenyToClubSerializer(serializers.Serializer):
    club_id = serializers.IntegerField()
    amount = serializers.IntegerField()


class PaymenyToClubConfirmSerializer(serializers.Serializer):
    invoice_id = serializers.IntegerField()
    card_id = serializers.IntegerField()


class RequestsGetSerializer(serializers.ModelSerializer):
    investor = InvestorSerializer
    class Meta:
        model = RequesteToJoinClub
        fields = (
            'id',
            'investor',
            'status'
        )


class ClubInvoiceGetSerializer(serializers.ModelSerializer):
    club = ClubNamesSerializer()
    class Meta:
        model = ClubInvoice
        fields = "__all__"


class ClubBankAccountInfoCreateSerialializer(serializers.ModelSerializer):
    class Meta:
        model = ClubBankAccountInfo
        fields = "__all__"


class ClubBankAccountInfoGetSerialializer(serializers.ModelSerializer):
    club = ClubGetSerializer()
    class Meta:
        model = ClubBankAccountInfo
        fields = "__all__"


class InvestorTransactionClubGetSerializer(serializers.ModelSerializer):
    investor = InvestorSerializer()
    invoice = InvestorSerializer()
    club = ClubGetSerializer()

    class Meta:
        model = InvestorTransactionClub
        fields = "__all__"


class ClubCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubCheck
        fields = "__all__"


class ClubCheckGetSerializer(serializers.ModelSerializer):
    investor = InvestorSerializer()
    invoice = InvestorSerializer()
    club = ClubGetSerializer()

    class Meta:
        model = ClubCheck
        fields = "__all__"


class ProjectPaymenyFromClubSerializer(serializers.Serializer):
    club_id = serializers.IntegerField()
    project_id = serializers.IntegerField() 
    amount = serializers.CharField()


class PaymentSerializerFromClub(serializers.Serializer):
    bank_account_id = serializers.CharField()
    invoice_id = serializers.IntegerField()