# Generated by Django 4.1.3 on 2023-12-16 16:48

from django.db import migrations, models
import scraping.models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0008_alter_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=scraping.models.filename),
        ),
    ]
