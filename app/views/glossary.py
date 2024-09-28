from collections import defaultdict
from django.db.models import Q, F
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.glossary import Glossary
from rest_framework.permissions import AllowAny


class GlossaryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Get the language from the query parameters, default to 'eng' if not provided
        language = request.query_params.get('language', 'en')
        search_query = request.query_params.get('q', '')  # Get the search query from query params
        category = request.query_params.get('category', None)  # Get the category from query params
        glossary_id = request.query_params.get('glossary_id', None)  # Get glossary_id from query params

        if language not in ['uz', 'ru', 'en']:
            return Response({'error': 'Invalid language code'}, status=status.HTTP_400_BAD_REQUEST)

        # If glossary_id is provided, return the specific glossary
        if glossary_id:
            try:
                glossary = Glossary.objects.get(id=glossary_id)
            except Glossary.DoesNotExist:
                return Response({'error': 'Glossary not found'}, status=status.HTTP_404_NOT_FOUND)

            # Prepare the glossary data for the specific glossary, including the image
            glossary_data = {
                'id': glossary.id,  # Add the glossary ID
                'name': getattr(glossary, f'name_{language}', ''),
                'description': getattr(glossary, f'description_{language}', ''),
                'image': glossary.image.url if glossary.image else None,  # Include the image
                'sections': [
                    {
                        'name': getattr(section, f'name_{language}', ''),
                        'description': getattr(section, f'description_{language}', ''),
                        'image': section.image.url if section.image else None  # Add section image
                    }
                    for section in glossary.glossarysection_set.all()
                ]
            }

            return Response(glossary_data, status=status.HTTP_200_OK)

        # Base queryset for multiple glossaries
        glossaries = Glossary.objects.all()

        # If category is provided, filter by category
        if category:
            glossaries = glossaries.filter(category=category)

        # If search query is provided, filter by glossary and glossary section fields
        if search_query:
            glossaries = glossaries.filter(
                # Search in glossary fields in all languages
                Q(name_uz__icontains=search_query) |
                Q(description_uz__icontains=search_query) |
                Q(name_ru__icontains=search_query) |
                Q(description_ru__icontains=search_query) |
                Q(name_en__icontains=search_query) |
                Q(description_en__icontains=search_query) |
                # Search in glossary section fields in all languages
                Q(glossarysection__name_uz__icontains=search_query) |
                Q(glossarysection__description_uz__icontains=search_query) |
                Q(glossarysection__name_ru__icontains=search_query) |
                Q(glossarysection__description_ru__icontains=search_query) |
                Q(glossarysection__name_en__icontains=search_query) |
                Q(glossarysection__description_en__icontains=search_query)
            ).distinct()

        # Sort glossaries by their name based on the selected language
        glossaries = glossaries.order_by(F(f'name_{language}').asc())

        # Group glossaries by their first letter
        grouped_data = defaultdict(list)

        for glossary in glossaries:
            glossary_name = getattr(glossary, f'name_{language}', '')
            first_letter = glossary_name[0].upper() if glossary_name else ''  # Get the first letter in uppercase

            # Prepare the glossary data
            glossary_data = {
                'id': glossary.id,  # Use the ID from the glossary object
                'name': glossary_name,
                'description': getattr(glossary, f'description_{language}', ''),
                'image': glossary.image.url if glossary.image else None,  # Add the image for the glossary
                'sections': [
                    {
                        'name': getattr(section, f'name_{language}', ''),
                        'description': getattr(section, f'description_{language}', ''),
                        'image': section.image.url if section.image else None  # Add the image for each section
                    }
                    for section in glossary.glossarysection_set.all()
                ]
            }
            # Group glossaries by the first letter
            grouped_data[first_letter].append(glossary_data)

        # Prepare the final response, sorted by first letter
        sorted_grouped_data = [{'first_letter': letter, 'glossaries': glossaries} for letter, glossaries in sorted(grouped_data.items())]

        return Response(sorted_grouped_data, status=status.HTTP_200_OK)
