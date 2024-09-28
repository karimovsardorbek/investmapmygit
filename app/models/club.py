from django.db import models
from django.apps import apps
from .investor import Investor
import os
from uuid import uuid4


def club_file_path(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("club-logo/", filename)


class Club(models.Model):
    FIXED_PRICE = 'fixed_price'
    PERCENTAGE = 'percentage'

    TYPE_CHOICES = [
        (FIXED_PRICE, 'Fixed Price'),
        (PERCENTAGE, 'Percentage'),
    ]
    logo = models.FileField(upload_to=club_file_path,null=True,blank=True)
    type = models.CharField(max_length=50, unique=True, choices=TYPE_CHOICES)
    investor = models.OneToOneField('app.Investor', related_name="club_owner", on_delete = models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    min_amount = models.DecimalField(max_digits=20, decimal_places=2)
    max_amount = models.DecimalField(max_digits=20, decimal_places=2)
    percentage = models.DecimalField(max_digits=2, decimal_places=2, null = True, blank=True)
    fixed_price = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank=True)
    members = models.ManyToManyField(Investor, related_name="member_club")
    name = models.CharField(max_length=255, default='')
    is_active = models.BooleanField(default=False)  # Default to False

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class RequesteToJoinClub(models.Model):
    class Status(models.TextChoices):
        APPROVED = "Approved", "Approved"
        REJECTED = "Rejected", "Rejected"
        CREATED = "Created", "Created"
    investor = models.ForeignKey(Investor,on_delete=models.CASCADE)
    club = models.ForeignKey(Club,on_delete=models.CASCADE)
    status = models.CharField(
        max_length=8, choices=Status.choices, default=Status.CREATED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.investor.user.first_name


class ClubBankAccountInfo(models.Model):
    club = models.ForeignKey(Club, related_name='bank_accounts', on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=34)  # IBAN numbers can be up to 34 characters
    account_holder_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    routing_number = models.CharField(max_length=9, null=True, blank=True)  # Optional, used in some countries

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_holder_name} - {self.bank_name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class ClubInvoice(models.Model):
    class Status(models.TextChoices):
        CREATED = "CRD", "Created"
        NOT_PAID = "NPD", "Not Paid"
        PAID = "PD","Paid"
        CANCELED = "CLD", "Cancelled"
        EXPIRED = "EXP","Expired"
 
    transation_id = models.CharField(max_length=100,null=True,blank=True)
    investor = models.ForeignKey(Investor, related_name='investor_club_invoice', on_delete=models.CASCADE)
    club = models.ForeignKey(Club, related_name='club_investor_invoice', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=3, choices=Status.choices, default=Status.NOT_PAID
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self) -> str:
        return super().__str__()


class ClubCheck(models.Model):
    invoice_id = models.ForeignKey(ClubInvoice,on_delete=models.CASCADE)
    investor = models.ForeignKey(Investor,on_delete=models.SET_NULL,null=True)
    club = models.ForeignKey(Club, related_name='club_investor_check', on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    amount = models.DecimalField(default=0,decimal_places=2,max_digits=20)
    payed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.club.name


class InvestorTransactionClub(models.Model):
    investor = models.ForeignKey(Investor, related_name='investor_club', on_delete=models.CASCADE, null=True, blank=True)
    club = models.ForeignKey(Club, related_name='investor_transaction_club', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    invoice = models.ForeignKey(ClubInvoice,on_delete=models.CASCADE,null=True,blank=True)  # Assuming 'View invoice' means downloading an invoice file.
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
    card_number = models.CharField(max_length=16, default='')

    def __str__(self):
        return f"Transaction by {self.investor.user.email} on {self.project.startup_name}"