# Generated by Django 5.1 on 2024-09-29 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Buildmate', '0013_offer_table_sale_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer_table',
            name='sale_price',
        ),
    ]
