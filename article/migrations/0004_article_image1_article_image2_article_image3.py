# Generated by Django 5.1.2 on 2024-10-26 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_article_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image1',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='image2',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='image3',
            field=models.URLField(blank=True, null=True),
        ),
    ]
