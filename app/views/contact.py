from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from ..models.contact import ContactDetails
from ..serializers.contact import ContactDetailsSerializer, SendQuestionSerializer
from drf_yasg.utils import swagger_auto_schema


class ContactDetailsView(APIView):
    permission_classes = [AllowAny] 

    def get(self, request, *args, **kwargs):
        contact_details = ContactDetails.objects.first()
        if not contact_details:
            return Response({"error": "Contact details not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ContactDetailsSerializer(contact_details)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SendQuestionCreateView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(request_body=SendQuestionSerializer)
    def post(self, request, *args, **kwargs):
        serializer = SendQuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Your request saved successfully. We will respond as soon as possible"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)