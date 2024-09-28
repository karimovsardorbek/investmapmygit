from django.db import models

class Testimonial(models.Model):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_eng = models.CharField(max_length=255)
    
    comment_uz = models.TextField()
    comment_ru = models.TextField()
    comment_eng = models.TextField()
    
    image = models.ImageField(upload_to='testimonials/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_uz