from django.db import models


class Statistics(models.Model):
    investor_count = models.PositiveIntegerField(default=0)  
    project_count = models.PositiveIntegerField(default=0)   
    description_uz = models.TextField()
    description_ru = models.TextField()
    description_eng = models.TextField()
    value = models.IntegerField()

    def __str__(self):
        return f"Statistics - Investors: {self.investor_count}, Projects: {self.project_count}"