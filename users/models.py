from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    GENDER_TYPES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    tel_number = models.CharField(max_length=13, blank=False, default='+380')
    gender = models.CharField(max_length=1, choices=GENDER_TYPES, default='M')
    nick_name = models.CharField(max_length=50, default=' ')
    is_master = models.BooleanField(default=False)