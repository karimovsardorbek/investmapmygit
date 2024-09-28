from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from ..models.application import Application
from ..models.approval import ApprovalHistory
from ..models.bank_secretary import BankSecretary
from ..serializers.application import ApplicationSerializer
from ..models.bank_council import BankMember, Meeting
from ..serializers.bank_council import BankMemberSerializer, MeetingSerializer
from rest_framework.generics import ListAPIView
from ..serializers.bank_secretary import BankSecretaryProfileSerializer
from user.notification import send_email, send_sms
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema

class BankSecretaryApprovalView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, application_id, *args, **kwargs):
        if not request.user.roles.filter(name='bank_secretary').exists():
            return Response({"error": "Only users with the 'bank_secretary' role can approve applications."},
                            status=status.HTTP_403_FORBIDDEN)

        bank_secretary = get_object_or_404(BankSecretary, user=request.user)

        application = get_object_or_404(Application, id=application_id, status='approved_by_moderator')

        status_choice = request.data.get('status')
        comment = request.data.get('comment', '')

        if status_choice not in ['approved', 'rejected']:
            return Response({"error": "Invalid status choice."}, status=status.HTTP_400_BAD_REQUEST)

        if status_choice == 'approved':
            application.status = 'approved_by_bank_secretary'
            application_status = "tasdiqlandi"
        else:
            application.status = 'returned_for_revision'
            application_status = "ko'rib chiqish uchun qaytarildi"

        application.current_checker = request.user
        application.save()

        ApprovalHistory.objects.create(
            application=application,
            status=status_choice,
            comment=comment,
            date_of_action=timezone.now(),
            executor_bank_secretary=bank_secretary
        )

        project_owner = application.project.company.created_by

        role = "bank sekretari"  
        message_text = f"Investmap.uz tizimidagi arizangiz {role} tomonidan {application_status}."

        send_sms(recipient=project_owner.phone_number, message=message_text)

        send_email(
            recipient=project_owner.email,
            message=message_text,
            subject="Application Status Update"
        )

        return Response({"message": f"Application has been {status_choice} by bank secretary."}, status=status.HTTP_200_OK)


class BankSecretaryPendingApplicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if not request.user.roles.filter(name='bank_secretary').exists():
            return Response({"error": "Only users with the 'bank_secretary' role can view applications."},
                            status=status.HTTP_403_FORBIDDEN)

        pending_applications = Application.objects.filter(status='approved_by_moderator')

        serializer = ApplicationSerializer(pending_applications, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CouncilMeetingListView(ListAPIView):
    serializer_class = MeetingSerializer

    def get_queryset(self):
        return Meeting.objects.filter(created_by=self.request.user)


class CouncilMeetingCreateView(APIView):
    @swagger_auto_schema(request_body=MeetingSerializer)
    def post(self, request, *args, **kwargs):
        serializer = MeetingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)  
            return Response({"message": "Council meeting created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BankMemberListView(ListAPIView):
    serializer_class = BankMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BankMember.objects.filter(created_by=self.request.user)


class BankMemberCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(request_body=BankMemberSerializer)
    def post(self, request, *args, **kwargs):
        serializer = BankMemberSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Bank member created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BankSecretaryProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            bank_secretary = BankSecretary.objects.get(user=request.user)
        except BankSecretary.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BankSecretaryProfileSerializer(bank_secretary)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=BankSecretaryProfileSerializer)
    def put(self, request, *args, **kwargs):
        try:
            bank_secretary = BankSecretary.objects.get(user=request.user)
        except BankSecretary.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BankSecretaryProfileSerializer(bank_secretary, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)