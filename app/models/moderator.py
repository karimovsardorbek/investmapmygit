from django.db import models
from user.models import CustomUser


class Moderator(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
