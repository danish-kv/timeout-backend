# Generated by Django 5.1.3 on 2024-12-02 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0014_leaverequest_comments'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leaverequest',
            old_name='comments',
            new_name='comment',
        ),
    ]
