# Generated by Django 5.1.2 on 2024-10-26 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_alter_article_ride'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='comments',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
