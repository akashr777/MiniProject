# Generated by Django 5.1 on 2024-10-02 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buildmate', '0017_alter_order_details_table_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_table',
            name='description',
            field=models.CharField(max_length=1000),
        ),
    ]
