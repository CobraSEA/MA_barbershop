from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GENDER_TYPES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    LEVELS = (
        ('J', 'Junior'),
        ('M', 'Middle'),
        ('S', 'Senior'),
        ('N', 'No level')
    )
    tel_number = models.CharField(max_length=13, blank=False, default='+380')
    gender = models.CharField(max_length=1, choices=GENDER_TYPES, default='M')
    birthday = models.DateField(default=date(1900, 1, 1))
    is_master = models.BooleanField(default=False)
    level = models.CharField(max_length=1, choices=LEVELS, default='N')
    nick_name = models.CharField(max_length=50, default=' ')

    def __str__(self):
        return self.username