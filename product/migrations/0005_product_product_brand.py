# Generated by Django 5.2.1 on 2025-06-09 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_brand',
            field=models.CharField(default='superpet', max_length=60),
        ),
    ]
