# Generated by Django 3.1.1 on 2020-10-13 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_auto_20201007_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='start_datetime',
            field=models.DateTimeField(),
        ),
    ]
