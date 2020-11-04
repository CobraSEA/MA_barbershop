# Generated by Django 3.1.1 on 2020-11-01 11:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0018_orders_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='MasterProcedure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('procedure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.procedures')),
            ],
            options={
                'unique_together': {('master_id', 'procedure_id')},
            },
        ),
    ]