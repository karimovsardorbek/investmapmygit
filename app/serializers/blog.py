from rest_framework import serializers
from ..models.blog import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'content', 'writer_full_name', 'writer_profile_photo', 'created_at']
