from rest_framework import serializers
from ..models.investor import Invoice, Card, CardImages


class BackgrounImageSerialize(serializers.ModelSerializer):
    class Meta:
        model = CardImages
        fields = "__all__"


class CardGetSerializer(serializers.ModelSerializer):
    background_image = BackgrounImageSerialize()
    class Meta:
        model = Card
        fields = ["id","card_name","owner","balance","expiration_date","vendor","card_number","investor","background_image","is_main"]


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__all__"


class CardAddSerialializer(serializers.Serializer):
    card_number = serializers.CharField()
    expiration_date = serializers.CharField()
    cardname  = serializers.CharField(required = False)


class ConfirmCardSerializer(serializers.Serializer):
    otp = serializers.CharField()
    cardId = serializers.CharField()


class InvoiceCreateSerializer(serializers.Serializer):
    amount = serializers.CharField()
    project_id = serializers.IntegerField()


class PaymentSerializer(serializers.Serializer):
    card_id = serializers.CharField()
    invoice_id = serializers.IntegerField()