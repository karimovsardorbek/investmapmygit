from django.db import models
from django.conf import settings
from .projects import Project
import os
from uuid import uuid4
from django.apps import apps


def invoices_file_path(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("invoices/", filename)


def investor_documents_file_path(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("investor_documents/", filename)


def card_image_file_path(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("card-images/", filename)


class Investor(models.Model):
    INVESTOR_TYPE_CHOICES = [
        ('business_angel', 'Business Angel'),
        ('venture_fund', 'Venture Fund'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='investor')
    investor_type = models.CharField(max_length=20, choices=INVESTOR_TYPE_CHOICES, default="")
    linkedin = models.URLField(max_length=255,null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.get_investor_type_display()}"


class ProjectInvestment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='investments')
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE, related_name='investments')
    amount = models.DecimalField(max_digits=20, decimal_places=2)  # Amount invested by the investor
    equity = models.DecimalField(max_digits=5, decimal_places=2)  # Equity the investor owns in the project

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Investor {self.investor.user.email} - {self.equity}% equity in {self.project.startup_name}"


class CardImages(models.Model):
    photo = models.FileField(upload_to=card_image_file_path)

    def __str__(self):
        return f"{self.photo.name}"


class Card(models.Model):
    userId = models.CharField()
    cardId = models.CharField(max_length=150)
    owner  = models.CharField(max_length=100)
    card_name = models.CharField(max_length=100,null=True,blank=True)
    card_number = models.CharField(max_length=16, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    expiration_date = models.CharField()
    bankid = models.IntegerField()
    vendor = models.CharField(max_length=100) 
    processing = models.CharField(max_length=100)
    investor = models.ForeignKey(Investor, related_name='bank_cards', on_delete=models.CASCADE)
    phone_number = models.CharField()
    is_active = models.BooleanField(default=True)
    background_image = models.ForeignKey(CardImages,on_delete=models.SET_NULL,null=True,blank=True)
    is_main = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.owner} - {self.card_number[-4:]}"  # Displaying only the last 4 digits for security

    def save(self, *args, **kwargs):
        super(Card, self).save(*args, **kwargs)


class BankAccountInfo(models.Model):
    investor = models.ForeignKey(Investor, related_name='bank_accounts', on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=34)  # IBAN numbers can be up to 34 characters
    account_holder_name = models.CharField(max_length=255)
    routing_number = models.CharField(max_length=9, null=True, blank=True)  # Optional, used in some countries

    def __str__(self):
        return f"{self.account_holder_name} - {self.bank_name}"


class InvestorDocument(models.Model):
    investor = models.ForeignKey(Investor, related_name='investor_documents', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to=investor_documents_file_path)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    class Status(models.TextChoices):
        CREATED = "CRD", "Created"
        NOT_PAID = "NPD", "Not Paid"
        PAID = "PD","Paid"
        CANCELED = "CLD", "Cancelled"
        EXPIRED = "EXP","Expired"
 
    transation_id = models.CharField(max_length=100,null=True,blank=True)
    investor = models.ForeignKey(Investor, related_name='invoice_investor', on_delete=models.CASCADE,null=True,blank=True)
    club = models.ForeignKey('app.Club',related_name='invoice_club',on_delete=models.CASCADE,null=True,blank=True)

    project = models.ForeignKey(Project, related_name='project_investor_invoice', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=3, choices=Status.choices, default=Status.NOT_PAID
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    def __str__(self) -> str:
        return self.project.startup_name
    
    def save(self, *args, **kwargs):
        if not self.investor and self.club:
            raise ValueError({'error':'Club or investor should be given'})
        super().save(*args, **kwargs)

class Check(models.Model):
    invoice_id = models.ForeignKey(Invoice,on_delete=models.CASCADE)
    investor = models.ForeignKey(Investor,on_delete=models.SET_NULL,null=True,blank=True)
    club = models.ForeignKey('app.Club',related_name='check_club',on_delete=models.SET_NULL,null=True,blank=True)

    project = models.ForeignKey(Project, related_name='check_project', on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    amount = models.DecimalField(default=0,decimal_places=2,max_digits=10)
    payed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.project.startup_name
    
    def save(self, *args, **kwargs):
        if not self.investor and self.club:
            raise ValueError({'error':'Club or investor should be given'})
        super().save(*args, **kwargs)

class Transaction(models.Model):
    investor = models.ForeignKey(Investor, related_name='investor_transaction', on_delete=models.CASCADE,null=True,blank=True)
    club = models.ForeignKey('app.Club',related_name='transaction_club',on_delete=models.CASCADE,null=True,blank=True)
    project = models.ForeignKey('app.Project', related_name='projects_investor', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE,null=True,blank=True)  # Assuming 'View invoice' means downloading an invoice file.
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
    card_number = models.CharField(max_length=16, default='')

    def __str__(self):
        return f"Transaction by {self.investor.user.email} on {self.project.startup_name} - {self.date.strftime('%Y-%m-%d')}"
    
    def save(self, *args, **kwargs):
        if not self.investor and self.club:
            raise ValueError({'error':'Club or investor should be given'})
        super().save(*args, **kwargs)