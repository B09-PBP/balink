# Generated by Django 5.1.2 on 2024-10-26 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_remove_userprofile_cart'),
        ('product', '0002_alter_product_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='privilege',
            new_name='user_privelege',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cart',
            field=models.ManyToManyField(blank=True, related_name='user_carts', to='product.product'),
        ),
    ]