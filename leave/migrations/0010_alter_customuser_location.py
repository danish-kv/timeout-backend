# Generated by Django 5.1.3 on 2024-12-02 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0009_remove_leaverequest_manager_leaverequest_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='location',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
