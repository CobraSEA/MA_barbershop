# Generated by Django 3.1.1 on 2020-10-04 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20201004_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='masters',
            name='nick_name',
            field=models.CharField(default=' ', max_length=50),
        ),
    ]
