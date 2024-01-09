# Generated by Django 4.1.4 on 2024-01-08 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
