# Generated by Django 5.0.1 on 2024-01-11 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0003_customerprofile_passport_photo_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomerProfile',
            new_name='Customer',
        ),
    ]
