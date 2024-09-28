from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
import os
import requests
import json
import redis
from decimal import Decimal
from rest_framework import status

from app.serializers.payment import (
    InvoiceSerializer,
    PaymentSerializer,
    InvoiceCreateSerializer,
    CardGetSerializer,
    CardAddSerialializer,
    ConfirmCardSerializer
)

from app.models.investor import (
    Investor,
    Invoice,
    Card,
    Transaction,
    Check,
    ProjectInvestment,
)

from rest_framework.views import APIView
from user.models import Role
from rest_framework.response import Response

redis_client = redis.StrictRedis(
    host=os.getenv('REDIS_HOST', '127.0.0.1'),
    port=int(os.getenv('REDIS_PORT', 6379)),    
    db=int(os.getenv('REDIS_DB', 0))            
)


class CreateCard(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CardAddSerialializer)  
    def post(self, request, *args, **kwargs):
        url = "https://dev.gw.paylov.uz/merchant/userCard/createUserCard/"
        card_number =  request.data.get("card_number")
        expiration_date = request.data.get("expiration_date")
        cardname = request.data.get("cardname")
        card_exist = False
        try:
            Card.objects.get(card_number = card_number)
            card_exist = True
        except Card.DoesNotExist:
            pass
        if card_exist:
            return Response({'error':"Card already exist"},status=status.HTTP_400_BAD_REQUEST)

        data = {
            "userId":os.getenv("MERCHAN_ID"),
            "cardNumber":card_number,
            "expireDate":expiration_date,
        }

        json_data = json.dumps(data)
        headers = {
            'Content-Type': 'application/json',
            'api-key': os.getenv("API_KEY"),
        }  
        response = requests.post(url, data=json_data, headers=headers)
        
        response_data = response.json()
        if response.status_code == 200:
            cid = response_data.get("result", {}).get("cid")
            otp_sent_phone = response_data.get("result", {}).get("otpSentPhone")
            data["cardname"] = cardname
            data["user"] = self.request.user.id
            data["cid"] = cid
            data["sendPhone"] = otp_sent_phone
                
            redis_client.setex(f"card_check:{self.request.user.id}", 120, json.dumps(data))
            return Response({'message':f"cid:{cid}"},status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error':response_data.get("error")},status=status.HTTP_400_BAD_REQUEST)

  
class ConfirmCard(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ConfirmCardSerializer)  
    def post(self, request, *args, **kwargs):
        url = "https://dev.gw.paylov.uz/merchant/userCard/confirmUserCardCreate/"

        user_data_json = redis_client.get(f"card_check:{self.request.user.id}")
        otp = request.data.get("otp")
        cardId = request.data.get("cardId")

        if not user_data_json:
            return Response({"error":"No such user creating card"})
        try:
            user_data = json.loads(user_data_json)
        except json.JSONDecodeError as e:
            return Response({"error": "Invalid data format in Redis", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if not user_data.get('cid')==cardId:
            return Response({"error":"card id is invalid"},status=status.HTTP_400_BAD_REQUEST)
        
        data = {
            "cardId": cardId,
            "otp":otp,
            "cardName":user_data.get("cardname")
        }
        user = self.request.user
        investor = Investor.objects.get(user = user)
        if not self.request.user.id == user_data.get("user"):
            return Response({'error':'this is not the user that is createing one'},status=status.HTTP_400_BAD_REQUEST)
        json_data =json.dumps(data)
        
        headers = {
            'Content-Type': 'application/json',
            'api-key': os.getenv("API_KEY"),
        }  
        response = requests.post(url, data=json_data, headers=headers)

        response_data = response.json()
        
        if response.status_code==200:
            response_data = response_data.get("result", {})
            response_data = response_data.get("card",{})
            try:
                balance = get_balance(response_data.get("balance"))
                print(balance)
                card = Card.objects.create(
                    userId = response_data.get("userId"),
                    cardId = response_data.get("cardId"),
                    owner = response_data.get("owner"), 
                    card_name = user_data.get("cardname"),
                    card_number = response_data.get("number"),
                    balance = balance,
                    expiration_date = response_data.get("expireDate"),
                    bankid = response_data.get("bankId"),
                    vendor = response_data.get("vendor"),
                    processing = response_data.get("processing"),
                    investor = investor,
                    phone_number = user_data.get("sendPhone"),
                )
                return Response({'message':"Card successfully added","userId":card.userId},status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error':("Exeption occured while creating Card"),"data":response_data},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            response_data = response_data.get("error",{})
            return Response({'error':response_data},status=status.HTTP_400_BAD_REQUEST)


class GetCard(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = self.request.user.investor
        url = "https://dev.gw.paylov.uz/merchant/userCard/getAllUserCards/"
        local_cards = Card.objects.filter(investor=user)
        
        if local_cards.exists():
            card = local_cards.first() 
            print("card", card.userId)
        else:
            return Response({'error': 'No cards found for this user.'}, status=status.HTTP_404_NOT_FOUND)
        
        headers = {
            'Content-Type': 'application/json',
            'api-key': os.getenv("API_KEY"),
        }
        url = f"https://dev.gw.paylov.uz/merchant/userCard/getAllUserCards/?userId={card.userId}"  
        response = requests.get(url, headers=headers)
        response_data = response.json()
        
        if response.status_code == 200:
            response_cards = response_data.get("result", {}).get("cards", [])
            local_card_ids = set(Card.objects.filter(investor=user).values_list('cardId', flat=True))
            
            updated_local_cards = []
            
            for response_card in response_cards:
                if response_card["cardId"] in local_card_ids:
                    try:
                        local_card = Card.objects.get(cardId=response_card["cardId"])
                        local_card.balance = get_balance(response_card["balance"])
                        local_card.save()
                        updated_local_cards.append(local_card)
                    except Card.DoesNotExist:
                        continue
            
            serializer = CardGetSerializer(updated_local_cards, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': response_data.get("error", {})}, status=status.HTTP_200_OK)

class PaymentForProject(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=InvoiceCreateSerializer)

    def post(self, request, *args, **kwargs):

        user = request.user

        if not user.roles.filter(name=Role.INVESTOR).exists():
            return Response({'error':'Investor role should be assigned'}, status=status.HTTP_401_UNAUTHORIZED)

        amount = request.data.get("amount")
        project_id = request.data.get("project_id")
        investor = Investor.objects.get(id = user.id)
        
        try:
            invoice = Invoice.objects.create(
                project_id = project_id,
                investor = investor,
                amount = amount
            )
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":InvoiceSerializer(invoice).data},status=status.HTTP_200_OK)


class CheckCreateForProject(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=PaymentSerializer)  
    def post(self, request, *args, **kwargs):
        
        card_id = request.data.get("card_id")
        invoice_id = request.data.get("invoice_id")
        
        if not invoice_id or not card_id:
            return Response({"error": "Card or Invoice Id is not given"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            invoice = Invoice.objects.get(id = invoice_id)
            card = Card.objects.get(id = card_id) 
        except Invoice.DoesNotExist or Card.DoesNotExist:
            return Response({'error':"invoice or card don't exist"},status=status.HTTP_400_BAD_REQUEST)
        
        if not card.investor == self.request.user.investor:
            return Response({"error":"Card is not belong to requested user"})
        
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
            create_Check(user=self.request.user.investor,invoice=invoice,card=card)
            create_transaction(user=self.request.user.investor,invoice=invoice,card=card)

            # Create project investment after payment is confirmed
            self.create_or_update_project_investment(invoice)
            
            return Response({"message":"Successfully Paid"})     

        else:
            return Response({'error': response_data.get("error","unexpexted error")}, status=status.HTTP_200_OK)


class DeleteCardApiView(APIView):
    def delete(self, request, *args, **kwargs):
        id = kwargs.get('card_id')
        if not id:
            return Response({"error": "Card ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = self.request.user.investor
        
        try:
            card = Card.objects.get(investor = user,id = id)
        except Card.DoesNotExist as e:
            return Response({"error":"invalid Card ID"},status=status.HTTP_400_BAD_REQUEST)
        
        headers = {
            'Content-Type': 'application/json',
            'api-key': os.getenv("API_KEY"),
        }
        url = f"https://dev.gw.paylov.uz/merchant/userCard/deleteUserCard/?userCardId={card.cardId}"
        response = requests.delete(url,headers=headers)
        
        if response.status_code == 200:
            card.delete()
            return Response({"message":"Card successfully deleted"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error":"Error while deleting card"},status=status.HTTP_503_SERVICE_UNAVAILABLE)


def create_transaction(user, invoice,card):
    check = Transaction.objects.create(
        invoice=invoice,
        investor=user,
        amount = invoice.amount,
        project =  invoice.project,
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


def create_Check(user, invoice, card):
    check = Check.objects.create(
        invoice_id=invoice,
        investor=user,
        amount = invoice.amount,
        card_number=card.card_number,
        project =  invoice.project
    )
    return check


def decimal_to_float(d):
    if isinstance(d, Decimal):
        return float(d)
    raise TypeError("Expected a Decimal")



def get_balance(balance):
    return int(balance)/100


def create_or_update_project_investment(self, invoice):
    project = invoice.project  # Assuming the invoice has a relation to the project
    investor = self.request.user.investor
    amount = invoice.amount
    # Calculate the equity based on the current amount invested
    project_equity = project.equity
    funding_goal = project.funding_goal
    if funding_goal > 0:
        equity_percentage = (amount / funding_goal) * project_equity
    else:
        equity_percentage = 0
    # Check if the investor already has an investment in the project
    investment, created = ProjectInvestment.objects.get_or_create(
        project=project, investor=investor,
        defaults={'amount': amount, 'equity': equity_percentage}
    )
    if not created:
        # Update the existing investment
        investment.amount += amount
        investment.equity += equity_percentage
        investment.save()
    return investment