# Generated by Django 4.1.3 on 2022-11-09 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0002_alter_post_description_alter_post_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('body', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='is_public',
            field=models.BooleanField(default=True),
        ),
    ]
