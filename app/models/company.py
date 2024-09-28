from django.conf import settings
from django.db import models
import os 
from uuid import uuid4


def company_logos_file_path(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("company_logos/", filename)


class Company(models.Model):
    # Main Information
    logo = models.ImageField(upload_to=company_logos_file_path, blank=True, null=True)
    legal_name = models.CharField(max_length=255)
    TIN = models.CharField(max_length=255)  # Taxpayer Identification Number
    date_of_registration = models.DateField()
    national_classifier_of_activities = models.CharField(max_length=255)
    legal_address = models.CharField(max_length=500)
    name_of_director = models.CharField(max_length=255)
    director_TIN = models.CharField(max_length=255)
    share_capital = models.DecimalField(max_digits=255, decimal_places=2)
    state_of_activity = models.CharField(max_length=255)
    number_of_employees = models.PositiveIntegerField()

    # Bank Details
    name_of_bank = models.CharField(max_length=255)
    MFO = models.CharField(max_length=255)
    account_number_1 = models.CharField(max_length=255)
    account_number_2 = models.CharField(max_length=255, default="")

    # Contact Information
    contact_phone_number_1 = models.CharField(max_length=15)
    contact_phone_number_2 = models.CharField(max_length=15, default="")
    accountant_phone_number = models.CharField(max_length=15)
    international_contact_number = models.CharField(max_length=20, default="")
    email_address = models.EmailField()
    website = models.URLField(max_length=255, default="")
    legal_address_of_company = models.CharField(max_length=500)
    physical_address_of_company = models.CharField(max_length=500)

    # User who created the company
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,        
        related_name='created_companies'
    )

    def __str__(self):
        return self.legal_name