from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import ListAPIView
from ..models.application import Application, ApplicationNotification
from ..models.approval import ApprovalHistory
from ..models.moderator import Moderator

from ..serializers.moderator import (
    ModeratorReviewSerializer, 
    ModeratorUpdateSerializer, 
    ModeratorProfileSerializer,
)

from ..serializers.application import (
    ApplicationDetailSerializer, 
    ApplicationNotificationSerializer,
)

from ..models.projects import Project
from ..serializers.projects import ProjectSerializer
from user.notification import send_email, send_sms
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from ..models.club import Club
from ..serializers.club import ClubBankAccountInfoCreateSerialializer
from django.shortcuts import get_object_or_404


class ModeratorReviewView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ModeratorReviewSerializer)
    def post(self, request, application_id, *args, **kwargs):
        try:
            application = Application.objects.get(id=application_id)
        except Application.DoesNotExist:
            return Response({"error": "Application not found."}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.roles.filter(name='moderator').exists():
            return Response({"error": "Only users with the 'moderator' role can review this application."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = ModeratorReviewSerializer(data=request.data)
        if serializer.is_valid():
            status_choice = request.data.get('status')
            comment = request.data.get('comment', '')

            if status_choice not in ['approved', 'rejected', 'returned_for_revision']:
                return Response({"error": "Invalid status choice."}, status=status.HTTP_400_BAD_REQUEST)

            if status_choice == 'approved':
                application.status = 'visible'
                application_status = "tasdiqlandi"
            elif status_choice == 'rejected':
                application.status = 'rejected'
                application_status = "rad etildi"
            else:
                application.status = 'returned_for_revision'
                application_status = "ko'rib chiqish uchun qaytarildi"

            application.current_checker = request.user
            application.save()

            ApprovalHistory.objects.create(
                application=application,
                executor_moderator=request.user.moderator if hasattr(request.user, 'moderator') else None,
                status=status,
                comment=comment,
                date_of_action=timezone.now()  
            )

            project_owner = application.project.company.created_by

            role = "moderator"
            message_text = f"Investmap.uz tizimidagi arizangiz {role} tomonidan {application_status}."

            send_sms(recipient=project_owner.phone_number, message=message_text)

            send_email(
                recipient=project_owner.email,
                message=message_text,
                subject="Application Status Update"
            )

            if status_choice == 'approved':
                return Response({"message": "Application approved successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Application returned for revision."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModeratorApplicationListView(ListAPIView):
    serializer_class = ApplicationDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if not user.roles.filter(name='moderator').exists():
            return Application.objects.none()

        return Application.objects.filter(status__in=['under_review'])
 

class ModeratorUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Moderator.objects.get(user=self.request.user)
        except Moderator.DoesNotExist:
            return None
        
    @swagger_auto_schema(request_body=ModeratorUpdateSerializer)
    def put(self, request, *args, **kwargs):
        moderator = self.get_object()
        if not moderator:
            return Response({"error": "Moderator not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ModeratorUpdateSerializer(moderator, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Account details updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ModeratorProjectListView(ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if not user.roles.filter(name='moderator').exists():
            return Project.objects.none()

        return Project.objects.all()
    

class ModeratorProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            moderator = Moderator.objects.get(user=request.user)
        except Moderator.DoesNotExist:
            return Response({"error": "Moderator profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ModeratorProfileSerializer(moderator)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ApplicationNotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if not request.user.roles.filter(name='moderator').exists():
            return Response({"error": "Only moderators can view application notifications."},
                            status=status.HTTP_403_FORBIDDEN)

        notifications = ApplicationNotification.objects.all()
        serializer = ApplicationNotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class AddBankAccountForClub(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(request_body=ClubBankAccountInfoCreateSerialializer)
    def post(self, request, *args, **kwargs):
        if not request.user.roles == 'moderator':
            return Response({"detail": "Permission denied. Only moderators can add bank accounts."}, status=status.HTTP_403_FORBIDDEN)

        club_id = request.data.get('club_id')
        club = get_object_or_404(Club, id=club_id)

        if not club.is_active:
            return Response({"detail": "Club is not active."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ClubBankAccountInfoCreateSerialializer(data=request.data)

        if serializer.is_valid():
            serializer.save(club=club)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)