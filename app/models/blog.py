from django.db import models
from uuid import uuid4
import os


def blog_images_file_path(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("blog_images/", filename)


def writer_photos_file_path(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("writer_photos/", filename)


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=blog_images_file_path)
    content = models.TextField()
    writer_full_name = models.CharField(max_length=255, blank=True, null=True)
    writer_profile_photo = models.ImageField(upload_to=writer_photos_file_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title