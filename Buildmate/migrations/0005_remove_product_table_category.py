# Generated by Django 5.1 on 2024-09-08 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Buildmate', '0004_category_table_product_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product_table',
            name='category',
        ),
    ]
