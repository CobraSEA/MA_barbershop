from django.conf import settings
from django.db import models


class Masters(models.Model):
    LEVELS = (
        ('J', 'Junior'),
        ('M', 'Middle'),
        ('S', 'Senior'),
    )
    master = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    level = models.CharField(max_length=1, choices=LEVELS, default='J')
    nick_name = models.CharField(max_length=50, default=' ')


class Procedures(models.Model):
    name = models.CharField(max_length=50, blank=False)
    price = models.DecimalField(max_length=19, decimal_places=2, max_digits=19)
    duration = models.IntegerField(default=30)


class Works(models.Model):
    WORK_STATUSES = (
        ('P', 'planed'),
        ('D', 'done'),
        ('C', 'canceled'),
    )
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # master = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    master = models.ForeignKey(Masters, on_delete=models.CASCADE, default=1)
    procedure = models.ForeignKey(Procedures, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=WORK_STATUSES, default='P')


class Comments(models.Model):
    master = models.ForeignKey(Works, on_delete=models.CASCADE)
    mark = models.SmallIntegerField(default=5)
    text = models.TextField(default=' ')
