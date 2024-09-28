from django.db import models
from django.conf import settings
from django.apps import apps


class Bank(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Criteria(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    title = models.CharField(max_length=255)
    criteria = models.ManyToManyField(Criteria, related_name='positions')

    def __str__(self):
        return self.title


class BankMember(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_bank_members', null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.position.title}"


class BankCouncil(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(BankMember, related_name='councils')

    def __str__(self):
        return self.name


class Meeting(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    selected_members = models.ManyToManyField(BankMember, related_name='meetings')
    selected_applications = models.ManyToManyField('app.Application', related_name='meetings')
    status = models.CharField(max_length=50, choices=[('upcoming', 'Upcoming'), ('completed', 'Completed')], default='upcoming')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_bank_council_meeting', null=True, blank=True)

    def __str__(self):
        return f"Meeting {self.name} on {self.date}"