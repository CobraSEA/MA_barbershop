# Generated by Django 3.1.1 on 2020-11-21 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0020_auto_20201102_1216'),
    ]

    operations = [
        migrations.AddField(
            model_name='procedures',
            name='procedure_pic',
            field=models.ImageField(blank=True, null=True, upload_to='procedures/'),
        ),
    ]