from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import AllowAny
from ..models.aboutus import AboutUs, Oferta
from ..serializers.aboutus import AboutUsSerializer
from rest_framework.views import APIView


class AboutUsListView(generics.ListAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    permission_classes = [AllowAny]


class OfertaHTMLView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        oferta = Oferta.objects.first()  # Assuming you have only one Oferta
        if oferta:
            return HttpResponse(oferta.content, content_type='text/html')
        else:
            return HttpResponse('<h1>No Oferta Found</h1>', content_type='text/html')