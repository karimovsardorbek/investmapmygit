from django.db import models
import os
from uuid import uuid4


def about_us_file_path(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("about_us/", filename)


class AboutUs(models.Model):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_eng = models.CharField(max_length=255)
    
    description_uz = models.TextField()
    description_uz_ru = models.TextField()
    description_uz_eng = models.TextField()
    
    image = models.ImageField(upload_to=about_us_file_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title_uz
    

class Oferta(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()  # Store HTML content
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title