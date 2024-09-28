from rest_framework import serializers
from ..models.aboutus import AboutUs, Oferta


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = ['id', 'title_uz', 'title_ru', 'title_eng', 'description_uz', 'description_uz_ru', 'description_uz_eng', 'image', 'created_at']


def to_representation(self, instance):
    request = self.context.get('request')
    language = request.META.get('HTTP_ACCEPT_LANGUAGE', 'en').lower() 

    image_url = instance.image.url if instance.image else None

    if 'uz' in language:
        return {
            'id': instance.id,
            'title': instance.title_uz,
            'description': instance.description_uz,
            'image': image_url,
            'created_at': instance.created_at,
        }
    elif 'ru' in language:
        return {
            'id': instance.id,
            'title': instance.title_ru,
            'description': instance.description_uz_ru,  
            'image': image_url,
            'created_at': instance.created_at,
        }
    else:  
        return {
            'id': instance.id,
            'title': instance.title_eng,
            'description': instance.description_uz_eng,  
            'image': image_url,
            'created_at': instance.created_at,
        }


class OfertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oferta
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']