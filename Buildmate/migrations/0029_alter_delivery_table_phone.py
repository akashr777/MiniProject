# Generated by Django 5.1 on 2024-10-16 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buildmate', '0028_alter_order_details_table_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery_table',
            name='phone',
            field=models.BigIntegerField(),
        ),
    ]
