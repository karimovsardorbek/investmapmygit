from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.blog import BlogPost
from ..serializers.blog import BlogPostSerializer
from rest_framework.permissions import AllowAny


class BlogPostListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        blog_posts = BlogPost.objects.all().order_by('-created_at')  
        serializer = BlogPostSerializer(blog_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
