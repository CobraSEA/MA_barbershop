from django.contrib.auth.models import User
from django.db import models

class masters(models.Model):
    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20, blank=False)
    nic_name = models.CharField(max_length=20, blank=False)

class procedures(models.Model):
    name = models.CharField(max_length=50, blank=False)
    price = models.DecimalField(max_length=19, decimal_places=2, max_digits=19)
    duration = models.IntegerField(default=30)

class clients(models.Model):
    SEX_TYPES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, blank=False)
    birthday = models.DateField()
    sex = models.CharField(max_length=1, choices=SEX_TYPES)

