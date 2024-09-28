from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..models.projects import Project
from ..serializers.projects import ProjectSerializer

from ..models.bank_council import (
    BankMember, 
    Meeting, 
    BankCouncil,
)

from ..serializers.bank_council import (
    MeetingSerializer, 
    BankMemberSerializer, 
    BankCouncilSerializer,
)

from ..models.application import ApplicationScore, Application
from ..serializers.application import ApplicationSerializer, ApplicationScoreSerializer
from user.notification import send_sms, send_email
from drf_yasg.utils import swagger_auto_schema


class BankCouncilMemberProjectsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        projects = Project.objects.filter(applications__status='visible')
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class BankCouncilMeetingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            bank_member = BankMember.objects.get(user=request.user)
        except BankMember.DoesNotExist:
            return Response({"error": "Bank Council Member not found."}, status=status.HTTP_404_NOT_FOUND)

        meetings = Meeting.objects.filter(selected_members=bank_member)

        serializer = MeetingSerializer(meetings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BankCouncilMeetingDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, meeting_id, *args, **kwargs):
        try:
            meeting = Meeting.objects.get(id=meeting_id)
        except Meeting.DoesNotExist:
            return Response({"error": "Meeting not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MeetingSerializer(meeting)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApplicationScoringView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ApplicationScoreSerializer)  
    def post(self, request, application_id, *args, **kwargs):
        application = get_object_or_404(Application, id=application_id, status='approved_by_bank_secretary')

        try:
            bank_member = BankMember.objects.get(user=request.user)
        except BankMember.DoesNotExist:
            return Response({"error": "Bank Member not found."}, status=status.HTTP_404_NOT_FOUND)

        allowed_criteria = bank_member.position.criteria.all()

        serializer = ApplicationScoreSerializer(data=request.data.get('scores'), many=True)
        if serializer.is_valid():
            for entry in serializer.validated_data:
                if entry['criteria_score'] not in allowed_criteria:
                    return Response({"error": "Invalid criteria for this bank member."}, status=status.HTTP_400_BAD_REQUEST)

                ApplicationScore.objects.update_or_create(
                    application=application,
                    member=bank_member,
                    criteria_score=entry['criteria_score'],
                    defaults={'score': entry['score'], 'comment': entry.get('comment')}
                )

            total_members = bank_member.position.criteria.count()
            total_scores = ApplicationScore.objects.filter(application=application).count()

            if total_scores == total_members * allowed_criteria.count():
                average_score = application.calculate_average_score()
                if average_score >= 9:
                    application_status = "tasdiqlandi"  
                else:
                    application_status = "qabul qilinmadi" 

                project_owner = application.project.company.created_by
                role = "bank konsul"

                message_text = f"Investmap.uz tizimidagi arizangiz {role} tomonidan {application_status}."

                send_sms(recipient=project_owner.phone_number, message=message_text)

                send_email(
                    recipient=project_owner.email,
                    message=message_text,
                    subject="Application Status Update"
                )

                return Response({"message": f"Scores submitted and application status updated to '{application_status}'."}, status=status.HTTP_200_OK)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BankCouncilMemberProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            bank_member = BankMember.objects.get(user=request.user)
        except BankMember.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BankMemberSerializer(bank_member)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=BankMemberSerializer)  
    def put(self, request, *args, **kwargs):
        try:
            bank_member = BankMember.objects.get(user=request.user)
        except BankMember.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BankMemberSerializer(bank_member, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApprovedByBankSecretaryView(ListAPIView):
    queryset = Application.objects.filter(status='approved_by_bank_secretary')
    serializer_class = ApplicationSerializer


class ApplicationsByBankMemberView(ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            bank_member = BankMember.objects.get(user=self.request.user)
        except BankMember.DoesNotExist:
            return Application.objects.none()

        return Application.objects.filter(meetings__selected_members=bank_member).distinct()


class CouncilMembersView(ListAPIView):
    serializer_class = BankCouncilSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            bank_member = BankMember.objects.get(user=user)
            return BankCouncil.objects.filter(members=bank_member)
        except BankMember.DoesNotExist:
            return BankCouncil.objects.none()