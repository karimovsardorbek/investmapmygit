from django.db import models
from user.models import CustomUser
from .bank_council import Bank


class BankSecretary(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email