from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.http import JsonResponse
from django.db.models import Sum, Q
from rest_framework import status
from app.models.application import Application
from ..models.investor import (
    Transaction, 
    BankAccountInfo, 
    InvestorDocument,
    Investor,
)

from ..serializers.investor import (
    TransactionSerializer,
    BankAccountInfoSerializer, 
    InvestorDocumentSerializer,
    InvestorSerializer,
    InvesterUpdateSerializer,
    InvestorProfileSerializer
)

from app.models.club import(
    Club
)

from ..models.projects import Project
from ..serializers.projects import ProjectListInvestorSerializer


class BankAccountInfoListView(ListCreateAPIView):
    serializer_class = BankAccountInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BankAccountInfo.objects.filter(investor=self.request.user.investor)


class InvestorDocumentView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = InvestorDocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InvestorDocument.objects.filter(investor=self.request.user.investor)
    
    @swagger_auto_schema(request_body=InvestorDocumentSerializer)
    def perform_create(self, serializer):
        serializer.save(investor=self.request.user.investor)


class AllTransactionsListView(ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [AllowAny] 


class TransactionListView(ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'investor'):
            return Transaction.objects.filter(investor=self.request.user.investor)
        return Transaction.objects.none()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class BusinessAngelInvestorListView(ListAPIView):
    serializer_class = InvestorSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        investor_type = self.request.query_params.get('type', 'business_angel')
        return Investor.objects.filter(investor_type=investor_type)


class VentureFundInvestorListView(ListAPIView):
    serializer_class = InvestorSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        investor_type = self.request.query_params.get('type', 'venture_fund')
        return Investor.objects.filter(investor_type=investor_type)
    

class ProjectsInvestorView(ListAPIView):
    serializer_class = ProjectListInvestorSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated investors can access

    def get_queryset(self):
        investor = self.request.user.investor
        
        project_ids = Transaction.objects.filter(investor=investor).values_list('project', flat=True)

        return Project.objects.filter(applications__status='visible', id__in=project_ids).distinct()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class InvestorUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Investor.objects.get(user=self.request.user)
        except Investor.DoesNotExist:
            return None
        
    @swagger_auto_schema(request_body=InvesterUpdateSerializer)
    def put(self, request, *args, **kwargs):
        investor = self.get_object()
        if not investor:
            return Response({"error": "Moderator not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = InvesterUpdateSerializer(investor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Account details updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvestorProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id,*args, **kwargs):

        try:
            investor = Investor.objects.get(user__id=id)
        except Investor.DoesNotExist:
            return Response({"error": "Investor profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = InvestorProfileSerializer(investor)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DashBordApiView(APIView):
    def get(self, request, *args, **kwargs):
        user =  self.request.user
        investor = Investor.objects.get(user=user)
        total_invested_projects_count = Project.objects.filter(project_investor_invoice__investor=investor).distinct().count()
        total_invested_money = Transaction.objects.filter(investor=investor).aggregate(total=Sum('amount'))['total'] or 0
        total_transactions_count = Transaction.objects.filter(investor=investor).count()
        visible_projects_count = Application.objects.filter(status = 'visible').distinct().count()
        clubs = Club.objects.filter(is_active=True).count()
        clubs_member = Club.objects.filter(
                Q(investor=investor) | Q(members=investor)
            ).count()
        
        return JsonResponse({
            'total_invested_projects_count': total_invested_projects_count,
            'total_invested_money': total_invested_money,
            'total_transactions_count': total_transactions_count,
            'visible_projects_count': visible_projects_count,
            'number_of_clubs':clubs,
            'my_clubs': clubs_member
        })