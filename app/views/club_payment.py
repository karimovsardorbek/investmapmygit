from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
import os
import requests
import json
from decimal import Decimal

from ..models.investor import (
    Card,
    Invoice,
    Check,
    Investor,
    Transaction
)

from ..serializers.payment import(
    InvoiceSerializer,
)

from app.models.club import(
    Club,
    ClubBankAccountInfo,
    ClubCheck,
    ClubInvoice,
    InvestorTransactionClub,  
)

from app.serializers.club import(
    PaymenyToClubSerializer,
    PaymenyToClubConfirmSerializer,
    InvestorTransactionClubGetSerializer,
    ProjectPaymenyFromClubSerializer,
    PaymentSerializerFromClub
)


class PaymentForClubApiView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=PaymenyToClubSerializer)
    def post(self, request):
        club_id = request.data.get('club_id')
        amount = request.data.get('amount')

        if not club_id or not amount:
            return Response({"error": "Club ID and amount are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            club = Club.objects.get(id=club_id)
        except Club.DoesNotExist:
            return Response({"error": "Club does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        investor = request.user.investor

        if club.investor != investor:
            return Response({"error": "Only the club owner can create invoices"}, status=status.HTTP_403_FORBIDDEN)
        if club.max_amount < amount:
            return Response({"error": "Amount is more that max amount on club"}, status=status.HTTP_400_BAD_REQUEST)
        if club.is_active == False:
            return Response({"error": "Club is not active yet"}, status=status.HTTP_404_NOT_FOUND)

        try:
            ClubBankAccountInfo.objects.get(club = club)
        except ClubBankAccountInfo.DoesNotExist:
            return Response({'error':'Club should own Bank Account'},status=status.HTTP_400_BAD_REQUEST)

        members = club.members.all()
        invoices = []
        
        for member in members:
            club_invoice = ClubInvoice.objects.create(
                investor=member,
                club=club,
                amount=amount,
                status=ClubInvoice.Status.NOT_PAID
            )
            invoices.append(club_invoice.id)

        return Response({"message": "Invoices created successfully", "invoice_ids": invoices}, status=status.HTTP_201_CREATED)


class PaymentConfirmForClub(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=PaymenyToClubConfirmSerializer)  
    def post(self, request, *args, **kwargs):
        
        card_id = request.data.get("card_id")
        invoice_id = request.data.get("invoice_id")
        
        user = request.user
        investor = Investor.objects.get(id = user.id)

        if not invoice_id or not card_id:
            return Response({"error": "Card or Invoice Id is not given"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            invoice = ClubInvoice.objects.get(id = invoice_id)
            card = Card.objects.get(id = card_id) 
        except ClubInvoice.DoesNotExist or Card.DoesNotExist:
            return Response({'error':"invoice or card don't exist"},status=status.HTTP_400_BAD_REQUEST)
        
        if not card.investor == investor:
            return Response({"error":"Card is not belong to requested user"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            transaction_id = get_transaction_id(invoice.amount)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        url = "https://dev.gw.paylov.uz/merchant/receipts/pay/"
        headers = {
            'Content-Type': 'application/json',
            'api-key': os.getenv("API_KEY"),
        }
        data = {
            "userId": os.getenv("MERCHAN_ID"),
            "transactionId": transaction_id,
            "cardId": card.cardId
        }
            
        json_data = json.dumps(data)

        response = requests.post(url, data=json_data, headers=headers)
        response_data = response.json()

        if response.status_code == 200:
            invoice.status = invoice.Status.PAID
            invoice.transation_id = transaction_id
            invoice.save()
            create_Check_club(user=investor,invoice=invoice,card=card)
            update_bank_accound(club=invoice.club,amount=invoice.amount)
            create_transaction_club(user=investor,invoice=invoice,card=card)
            return Response({"message":"Successfully Paid"},status=status.HTTP_202_ACCEPTED)     
        else:
            return Response({'error': response_data.get("error","unexpexted error")}, status=status.HTTP_400_BAD_REQUEST)


class GetTransactionsClubApiView(ListAPIView):
    serializer_class = InvestorTransactionClubGetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        investor = Investor.objects.get(user=user)    
        return InvestorTransactionClub.objects.filter(investor = investor)


class GetInvoiceInvestor(ListAPIView):
    serializer_class = InvestorTransactionClubGetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        investor = InvestorTransactionClub.objects.get(user=user)    
        return InvestorTransactionClub.objects.filter(investor = investor)
    

class PaymentProjectFromClub(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(request_body=ProjectPaymenyFromClubSerializer)  
    def post(self, request, *args, **kwargs):
        club_id = request.data.get("club_id")
        amount = request.data.get("amount")
        project_id = request.data.get("club_id")

        user = request.user
        investor = Investor.objects.get(user = user)
        if not investor:
            return Response({'error':'Investor role should be assigned'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            club = Club.objects.get(id = club_id, investor = investor)
            bank_account = ClubBankAccountInfo.objects.get(club = club)
        except Club.DoesNotExist:
            return Response({'error':'Club does not exist'},status=status.HTTP_400_BAD_REQUEST)
        except ClubBankAccountInfo.DoesNotExist:
            return Response({'error':'Club should have bank account first'},status=status.HTTP_400_BAD_REQUEST)
        
        if bank_account.amount < amount:
            return Response({'error':'Club does not enough amount'},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            invoice = Invoice.objects.create(
                project_id = project_id,
                club = club,
                amount = amount
            )
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":InvoiceSerializer(invoice).data},status=status.HTTP_200_OK)


class CheckCreateForProjectFromClub(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=PaymentSerializerFromClub)  
    def post(self, request, *args, **kwargs):
        
        bank_id = request.data.get("bank_account_id")
        invoice_id = request.data.get("invoice_id")
        user = self.request.user
        investor = Investor.objects.get(user = user)
        
        if not investor:
            return Response({"error": "Investor role should be assigned"}, status=status.HTTP_400_BAD_REQUEST)
       
        try:
            invoice = Invoice.objects.get(id = invoice_id)
            club_bank = ClubBankAccountInfo.objects.get(id = bank_id) 
        except Invoice.DoesNotExist or ClubBankAccountInfo.DoesNotExist:
            return Response({'error':"Invoice or Bank_id don't exist"},status=status.HTTP_400_BAD_REQUEST)
        
        if not investor == club_bank.club.investor:
            return Response({'error':"Investor is not Club owner"},status=status.HTTP_400_BAD_REQUEST)
        
        if club_bank.amount < invoice.amount:
            return Response({'error':'Club does not enough amount'},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            invoice.status = Invoice.Status.PAID
            invoice.save()
            club_bank.amount -= invoice.amount
            club_bank.save()
            create_Check(club=club_bank.club,invoice =invoice,bank_account_name=club_bank.account_number)
            create_transaction(club=club_bank.club,invoice =invoice,bank_account_name=club_bank.account_number)
        except Exception:
            return Response({'error':'error while creating'},status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': 'Successfully tranfered'}, status=status.HTTP_200_OK)        


def create_transaction_club(user, invoice,card):
    check = InvestorTransactionClub.objects.create(
        invoice=invoice,
        investor=user,
        amount = invoice.amount,
        club =  invoice.club,
        card_number = card.card_number,
    )


def get_transaction_id(amount):
    url = "https://dev.gw.paylov.uz/merchant/receipts/create/"
    headers = {
        'Content-Type': 'application/json',
        'api-key': os.getenv("API_KEY"),
    }
    
    data = {
        "userId": os.getenv("MERCHAN_ID"),  
        "amount": decimal_to_float(amount),
        "account": {
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        print(response_data)
        if response.status_code == 200:
            return response_data['result']['transactionId']
        else:
            error_msg = response_data.get("error")
            raise ValueError(f"Failed to create transaction: {error_msg}")
    
    except requests.exceptions.RequestException as e:
        raise ValueError(f"An error occurred: {str(e)}")


def create_Check_club(user, invoice, card):
    check = ClubCheck.objects.create(
        invoice_id=invoice,
        investor=user,
        amount = invoice.amount,
        card_number=card.card_number,
        club =  invoice.club
    )
    return check


def update_bank_accound(club,amount):
    bank_account = ClubBankAccountInfo.objects.get(club = club)
    bank_account.amount+=amount
    bank_account.save()


def decimal_to_float(d):
    if isinstance(d, Decimal):
        return float(d)
    raise TypeError("Expected a Decimal")


def create_Check(club, invoice, bank_account_name):
    check = Check.objects.create(
        invoice_id=invoice,
        club=club,
        amount = invoice.amount,
        card_number=bank_account_name,
        project =  invoice.project
    )
    return check


def create_transaction(club, invoice,bank_account_name):
    check = Transaction.objects.create(
        invoice=invoice,
        club=club,
        amount = invoice.amount,
        project =  invoice.project,
        card_number = bank_account_name,
    )