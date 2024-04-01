from django.db import models
from app.manager import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils import timezone



# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    password =models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)


    USERNAME_FIELD = 'phone_no'
    REQUIRED_FIELDS = ['name', 'password']
    objects = CustomUserManager()


class Contacts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=10)
    contact_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=50, null=True, blank=True)



class SpamNumber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    spam_number = models.CharField(max_length=10, unique=True)

