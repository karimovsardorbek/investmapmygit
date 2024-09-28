from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager, 
    PermissionsMixin
)

import os
from uuid import uuid4
from django.db import models
from django.utils import timezone
from app.models.company import Company


def avatar_file_path(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("user-avatar/", filename)


class UniqueConfig(models.Model):
    otp_counter = models.PositiveIntegerField(default=0)


class Role(models.Model):
    COMPANY = 'company'
    INVESTOR = 'investor'
    INVESTOR_COMPANY = 'investing_company'
    MODERATOR = 'moderator'
    BANK_SECRETARY = 'bank_secretary'
    BANK_COUNCIL = 'bank_council'

    ROLE_CHOICES = [
        (COMPANY, 'Company'),
        (INVESTOR, 'Investor'),
        (INVESTOR_COMPANY, 'Investing Company'),
        (MODERATOR, 'Moderator'),
        (BANK_SECRETARY, 'Bank Secretary'),
        (BANK_COUNCIL, 'Bank Council')
    ]

    name = models.CharField(max_length=50, unique=True, choices=ROLE_CHOICES)

    def __str__(self):
        return self.get_name_display()


class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError('The Email or Phone Number must be set')
 
        if email:
            email = self.normalize_email(email)

        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, phone_number, password, **extra_fields)

    def create_superuser(self, email, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, phone_number, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    deposite = models.DecimalField(max_digits=15,decimal_places=2,null=True,blank=True)
    caunty = models.CharField(max_length=15,null=True,blank=True)
    region = models.CharField(max_length=15,null=True,blank=True)
    avatar = models.FileField(upload_to=avatar_file_path,null=True,blank=True)
    otp_counter = models.PositiveSmallIntegerField(default=0)
    otp_sent_time = models.DateTimeField(null=True, blank=True)
    otp_tried = models.BooleanField(default=False)
    otp_attempts = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    password = models.CharField(max_length=128)
    roles = models.ManyToManyField(Role, related_name='users')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.email if self.email else self.phone_number

    def save(self, *args, **kwargs):
        if not self.otp_sent_time:
            self.otp_sent_time = timezone.now()
        super().save(*args, **kwargs)
    

class UserDevice(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='devices')
    ip_address = models.GenericIPAddressField()
    login_method = models.CharField(max_length=12, choices=[('email', 'Email'), ('phone_number', 'Phone Number')])
    can_login = models.BooleanField(default=False)
    login_attempt_time = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.ip_address} - {self.login_method} - {'Successful' if self.can_login else 'Failed'}"

    class Meta:
        constraints = []  