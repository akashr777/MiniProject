# Generated by Django 5.1 on 2024-10-16 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buildmate', '0023_alter_offer_table_percentage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_table',
            name='price',
            field=models.FloatField(max_length=20),
        ),
    ]
