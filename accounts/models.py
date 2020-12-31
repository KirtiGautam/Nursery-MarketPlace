from django.db import models, IntegrityError
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from dateutil.relativedelta import relativedelta

from accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Nursery(models.Model):
    user = models.OneToOneField(
        User, related_name='Nursery', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
