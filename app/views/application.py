from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models.application import Application, ApplicationNotification
from ..models.projects import Project
from ..serializers.application import ApplicationSerializer
from drf_yasg.utils import swagger_auto_schema


class ApplicationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ApplicationSerializer)  
    def post(self, request, *args, **kwargs):

        if not request.user.roles.filter(name='company').exists():
            return Response({"error": "Only users with the 'company' role can create an application."},
                            status=status.HTTP_403_FORBIDDEN)

        project_id = request.data.get('project_id')
        if not project_id:
            return Response({"error": "Project ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            project = Project.objects.get(id=project_id, company=request.user.company)
        except Project.DoesNotExist:
            return Response({"error": "Project not found or you do not have permission to create an application for this project."},
                            status=status.HTTP_404_NOT_FOUND)

        application = Application.objects.create(
            project=project,
            status='under_review',  
            current_checker=None 
        )

        company_owner = request.user
        ApplicationNotification.objects.create(
            application=application,
            project_name=project.name,
            company_owner_first_name=company_owner.first_name,
            company_owner_last_name=company_owner.last_name
        )

        serializer = ApplicationSerializer(application)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ApplicationUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ApplicationSerializer)  
    def put(self, request, application_id, *args, **kwargs):

        if not request.user.roles.filter(name='company').exists():
            return Response({"error": "Only users with the 'company' role can update an application."},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            application = Application.objects.get(id=application_id, project__company=request.user.company)
        except Application.DoesNotExist:
            return Response({"error": "Application not found or you do not have permission to update this application."},
                            status=status.HTTP_404_NOT_FOUND)

        if application.status != 'returned_for_revision':
            return Response({"error": "You can only update an application that has been returned for revision."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = ApplicationSerializer(application, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)