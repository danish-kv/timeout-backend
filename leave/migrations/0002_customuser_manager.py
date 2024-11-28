# Generated by Django 4.2.7 on 2024-11-28 09:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='manager',
            field=models.ForeignKey(blank=True, limit_choices_to={'role': 'manager'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
