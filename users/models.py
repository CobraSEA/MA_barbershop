from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count, Sum
from django.utils import timezone

from shop.models import Comments


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
    nick_name = models.CharField(max_length=50, default=' ', blank=True)

    @property
    def age(self):
        return timezone.now().date().year - self.birthday.year

    @property
    def ratio(self):
        if self.is_master:
            avg_qwr = Comments.objects.values('master') \
                .annotate(rates=Count('rate'), sum_rate=Sum('rate')).filter(master=self)
            if avg_qwr:
                return round(avg_qwr[0]['sum_rate'] / avg_qwr[0]['rates'], 2)
        return None

    def __str__(self):
        return self.username
