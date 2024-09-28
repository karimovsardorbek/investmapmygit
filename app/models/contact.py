from django.db import models


class ContactDetails(models.Model):
    email1 = models.EmailField(max_length=255)
    email2 = models.EmailField(max_length=255, blank=True, null=True)
    phone_number1 = models.CharField(max_length=20)
    phone_number2 = models.CharField(max_length=20, blank=True, null=True)
    office_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Contact Details - {self.email1}"


class SendQuestion(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)  # Optional field
    message = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"