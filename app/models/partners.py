from django.db import models
from uuid import uuid4
import os


def partners_image_file_path(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("partners/", filename)


class Partner(models.Model):
    name = models.CharField(max_length=255)
    description_uz = models.TextField()
    description_ru = models.TextField()
    description_eng = models.TextField()
    logo = models.ImageField(upload_to=partners_image_file_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
