from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from app.utils.paginations import DefaultLimitOffSetPagination
from app.models.moderator import Moderator
from rest_framework import status

from app.models.club import(
    Club,
    RequesteToJoinClub,
    ClubBankAccountInfo
)

from app.models.investor import(
    Investor
)

from app.serializers.club import(
    ClubSerializer,
    ClubUpdateSerializer,
    ClubGetSerializer,
    ClubBankAccountInfoGetSerialializer,
    RequestsGetSerializer,
    RequestJoinCreateSerializer,
    RequestJoinUpdateSerializer,
    ApproveClubSerializer
)


class ClubUpdateCreateApiView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ClubSerializer)
    def post(self, request, *args, **kwargs):
        serializer = ClubSerializer(data=request.data)
        if serializer.is_valid():
            club = serializer.save(active=False)
            return Response(ClubSerializer(club).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(request_body=ClubUpdateSerializer)
    def put(self, request, *args, **kwargs):
        club = self.get_object()
        if not club:
            return Response({"error": "Club not found."}, status=status.HTTP_404_NOT_FOUND)
        if not club.investor == self.request.user.investor:
            return Response({'error':'Club is not belong to requested'})
        
        serializer = ClubUpdateSerializer(club, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Club details updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClubListApiView(ListAPIView):
    queryset = Club.objects.filter(is_active=True)
    serializer_class = ClubGetSerializer
    pagination_class = DefaultLimitOffSetPagination
    permission_classes = [IsAuthenticated]


class ClubListGetMyClubs(ListAPIView):
    serializer_class = ClubGetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the authenticated user's investor profile
        investor = self.request.user.investor

        # Filter clubs where the user is a member
        return Club.objects.filter(members=investor).distinct()


class JoinClubApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(request_body=RequestJoinCreateSerializer)
    def post(self, request):
        club_id = request.data.get('club_id')
        try:
            club = Club.objects.get(id=club_id)
        except Club.DoesNotExist:
            return Response({"detail": "Club not found."}, status=status.HTTP_404_NOT_FOUND)
        
        investor = request.user.investor
        
        if club.members.filter(id=investor.id).exists():
            return Response({"detail": "You are already a member of this club."}, status=status.HTTP_400_BAD_REQUEST)

        existing_request = RequesteToJoinClub.objects.filter(club=club, investor=investor).first()
        if existing_request:
            if existing_request.status == RequesteToJoinClub.Status.CREATED:
                return Response({"detail": "You already have a pending request to join this club."}, status=status.HTTP_400_BAD_REQUEST)
            elif existing_request.status == RequesteToJoinClub.Status.REJECTED:
                existing_request.status = RequesteToJoinClub.Status.CREATED
                existing_request.save()
                return Response({"detail": "Request to join the club has been submitted successfully."}, status=status.HTTP_201_CREATED)

        RequesteToJoinClub.objects.create(club=club, investor=investor, status=RequesteToJoinClub.Status.CREATED)

        return Response({"detail": "Request to join the club has been submitted successfully."}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=RequestJoinUpdateSerializer)
    def put(self, request):
        club_id = request.data.get('club_id')
        request_id = request.data.get('request_id')
        status_str = request.data.get('status')

        try:
            club = Club.objects.get(id=club_id)
            requesting = RequesteToJoinClub.objects.get(pk = request_id)
        except Club.DoesNotExist:
            return Response({"detail": "Club not found."}, status=status.HTTP_404_NOT_FOUND)
        except RequesteToJoinClub.DoesNotExist:
            return Response({"detail": "Request not found."}, status=status.HTTP_404_NOT_FOUND)
        
        investor = request.user.investor
        
        if club.members.filter(id=investor.id).exists():
            return Response({"detail": "You are already a member of this club."}, status=status.HTTP_400_BAD_REQUEST)
        if not requesting.club == club:
            return Response({"detail": "Club didn't match"}, status=status.HTTP_400_BAD_REQUEST)
        if not requesting.investor==investor:
            return Response({"detail": "You are not investor requested to join this club."}, status=status.HTTP_400_BAD_REQUEST)

        if status_str == 'approved':
            club.members == investor
            requesting.status = RequesteToJoinClub.Status.APPROVED
            club.save()
            requesting.save()
            return Response({"detail": "Request to join the club has been Approved successfully."}, status=status.HTTP_201_CREATED)
        elif status_str =='rejected':
            requesting.status = RequesteToJoinClub.Status.APPROVED
            requesting.save()
            return Response({"detail": "Request to join the club has been Rejected successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Status is unclear"}, status=status.HTTP_400_BAD_REQUEST)


class RequestsApiView(ListAPIView):
    serializer_class = RequestsGetSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultLimitOffSetPagination

    def get_queryset(self):
        investor = self.request.user.investor

        return RequesteToJoinClub.objects.filter(club__investor=investor).distinct()


class ModeratorNotApprovedClubs(ListAPIView):
    queryset = Club.objects.filter(is_active=False)
    serializer_class = ClubGetSerializer
    pagination_class = DefaultLimitOffSetPagination
    permission_classes = [IsAuthenticated]


class ApproveClubApiView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ApproveClubSerializer)
    def put(self, request):
        club_id = request.data.get('club_id')
        status_str = request.data.get('status')

        user = request.user
        try:
            Moderator.objects.get(user = user)
        except Moderator.DoesNotExist:
            return Response({'error':'Requested user is not a Moderator'},status=status.HTTP_401_UNAUTHORIZED)
        try:
            club = Club.objects.get(id=club_id)
        except Club.DoesNotExist:
            return Response({"error": "Club not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if status_str == 'approved':
            club.is_active = True
            club.save()
            return Response({"message": "Club Approved Successfully"}, status=status.HTTP_202_ACCEPTED)
        elif status_str == 'rejected':
            club.delete()
            return Response({"message": "Club Rejected Successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Status wrong"}, status=status.HTTP_400_BAD_REQUEST)


class BankAccountInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        club_id = request.data.get('club_id')
        user = request.user
        try:
            investor = Investor.objects.get(user = user)
            club = Club.objects.get(pk = club_id)
        except Investor.DoesNotExist:
            return Response({'error':'Requested user is not a Moderator'},status=status.HTTP_401_UNAUTHORIZED)
        
        if club.investor == investor:
            club_info = ClubBankAccountInfo.objects.get(club = club)
            return Response({'message':ClubBankAccountInfoGetSerialializer(club_info).data()},status=status.HTTP_200_OK)
        
        if club.members == investor:
            club_info = ClubBankAccountInfo.objects.get(club = club)
            return Response({'message':ClubBankAccountInfoGetSerialializer(club_info).data()},status=status.HTTP_200_OK)
        return Response({"error": "Status wrong"}, status=status.HTTP_400_BAD_REQUEST)