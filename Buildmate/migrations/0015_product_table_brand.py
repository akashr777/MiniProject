# Generated by Django 5.1 on 2024-09-29 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buildmate', '0014_remove_offer_table_sale_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_table',
            name='brand',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
