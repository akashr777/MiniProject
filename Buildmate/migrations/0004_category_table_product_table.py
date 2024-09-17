# Generated by Django 5.1 on 2024-09-08 08:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buildmate', '0003_seller_table_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='category_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
                ('details', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='product_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('stock', models.IntegerField(max_length=20)),
                ('price', models.IntegerField(max_length=20)),
                ('photo', models.FileField(upload_to='')),
                ('category', models.CharField(max_length=100)),
                ('CATEGORY', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buildmate.category_table')),
                ('SELLER', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buildmate.seller_table')),
            ],
        ),
    ]
