from rest_framework import serializers
from ..models.testimonials import Testimonial


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = [
            'id', 'title_uz', 'title_ru', 'title_eng',
            'comment_uz', 'comment_ru', 'comment_eng',
            'image', 'created_at', 'updated_at'
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        if request:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE', 'en')  
        else:
            language = 'en'  

        if 'uz' in language:
            return {
                'id': instance.id,
                'title': instance.title_uz,
                'comment': instance.comment_uz,
                'image': instance.image.url if instance.image else None,
                'created_at': instance.created_at,
                'updated_at': instance.updated_at,
            }
        elif 'ru' in language:
            return {
                'id': instance.id,
                'title': instance.title_ru,
                'comment': instance.comment_ru,
                'image': instance.image.url if instance.image else None,
                'created_at': instance.created_at,
                'updated_at': instance.updated_at,
            }
        else:  
            return {
                'id': instance.id,
                'title': instance.title_eng,
                'comment': instance.comment_eng,
                'image': instance.image.url if instance.image else None,
                'created_at': instance.created_at,
                'updated_at': instance.updated_at,
            }