import datetime
from django.conf import settings
from django.db import models


class Procedures(models.Model):
    name = models.CharField(max_length=50, blank=False)
    price = models.DecimalField(max_length=19, decimal_places=2, max_digits=19)
    duration = models.IntegerField(default=30)

    def __str__(self):
        return self.name


class Orders(models.Model):
    RATES = ((5, 'Excelent'), (4, 'Good'), (3, 'Not bad'), (2, 'Bad'), (1, 'Horribly'), (0, 'Not rated'))
    STATUSES = (
        ('P', 'planed'),
        ('D', 'done'),
        ('C', 'canceled'),
    )
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='work_client', on_delete=models.CASCADE)
    master = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='work_master', on_delete=models.CASCADE)
    procedure = models.ForeignKey(Procedures, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField(auto_now_add=False)
    status = models.CharField(max_length=1, choices=STATUSES, default='P')
    rate = models.SmallIntegerField(default=0, choices=RATES)


    @property
    def end_datetime(self):
        return self.start_datetime + datetime.timedelta(minutes=self.procedure.duration)


class Comments(models.Model):
    RATES = ((5, 'Excelent'), (4, 'Good'), (3, 'Not bad'), (2, 'Bad'), (1, 'Horribly'))
    master = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_master')
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_client')
    insert_datetime = models.DateTimeField(auto_now_add=True)
    rate = models.SmallIntegerField(default=5, choices=RATES)
    text = models.TextField(default=' ')

    def __str__(self):
        return self.text


class MasterProcedure(models.Model):
    master = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    procedure = models.ForeignKey(Procedures, on_delete=models.CASCADE)

    # class Meta:
    #     unique_together = ('master_id', 'procedure_id')
