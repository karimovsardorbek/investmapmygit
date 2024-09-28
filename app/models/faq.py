from django.db import models


class FAQ(models.Model):
    question_uz = models.CharField(max_length=500)
    question_ru = models.CharField(max_length=500)
    question_eng = models.CharField(max_length=500)

    answer_uz = models.TextField()
    answer_ru = models.TextField()
    answer_eng = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_eng
    

class RaisingContact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=50)
    project_name = models.CharField(max_length=50) 