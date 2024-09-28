from django.db import models
from uuid import uuid4
import os


def glossary_section_image_path(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("glossary_sections/", filename)


def glossary_image_path(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("glossaries/", filename)


class Glossary(models.Model):
    CATEGORY_CHOICES = [
        ('startup_ecosystem', 'Startup Ecosystem'),
        ('funding_investment', 'Funding and Investment'),
        ('technology_innovation', 'Technology and Innovation'),
        ('business_models', 'Business Models'),
        ('entrepreneurship', 'Entrepreneurship'),
        ('market_growth', 'Market and Growth'),
    ]

    name_uz = models.CharField(max_length=500)
    description_uz = models.TextField()
    name_ru = models.CharField(max_length=500)
    description_ru = models.TextField()
    name_en = models.CharField(max_length=500)
    description_en = models.TextField()
    image = models.ImageField(upload_to=glossary_image_path, blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='')  # Choice field for category

    def __str__(self):
        return self.name_en  


class GlossarySection(models.Model):
    glossary = models.ForeignKey(Glossary, on_delete=models.CASCADE)
    name_uz = models.CharField(max_length=500)
    description_uz = models.TextField()
    name_ru = models.CharField(max_length=500)
    description_ru = models.TextField()
    name_en = models.CharField(max_length=500)
    description_en = models.TextField()
    image = models.ImageField(upload_to=glossary_section_image_path, blank=True, null=True)

    def __str__(self):
        return self.name_en 