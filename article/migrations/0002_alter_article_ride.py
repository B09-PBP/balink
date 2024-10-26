# Generated by Django 5.1.2 on 2024-10-24 16:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
        ('product', '0002_alter_product_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='ride',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
    ]
