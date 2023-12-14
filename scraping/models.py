from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.crypto import get_random_string
import uuid
import os
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models.signals import post_save


# from django.contrib.sites.models import Site


def filename(instance, filename):
    if filename:
        ext = filename.split(".")[-1]  # Get the file extension
        new_filename = f"{uuid.uuid4().hex}.{ext}"
        base_path = f"{str(instance._meta.model_name).lower()}s/{ext.upper()}"  # Change this to your desired directory
        current_date = timezone.now().strftime("%Y-%m-%d")
        file = os.path.join(base_path, current_date, new_filename)

        return file
    else:
        return None


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    def get_absolute_url(self):
        return f"/category/{self.slug}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(null=True, blank=True, max_length=200)
    category = models.ManyToManyField(
        Category, related_name="post_category", blank=True
    )
    image = models.ImageField(upload_to="Image", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    views = models.IntegerField(default=0)
    tags = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    slug = models.SlugField(null=True, blank=True, max_length=200)
    is_public = models.BooleanField(default=True)

    def get_absolute_url(self):
        return f"/p/{self.slug}"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(uuid.uuid4())
        super(Post, self).save(*args, **kwargs)

    def next(self):
        return self.get_next_by_date()

    def pre(self):
        return self.get_previous_by_date()


class Page(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(uuid.uuid4())

        super(Page, self).save(*args, **kwargs)


# Contact
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    readed = models.DateTimeField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Link(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=500)
    footer = models.BooleanField(null=True, blank=True)
    header = models.BooleanField(null=True, blank=True)
    new_tab = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Settings(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=150)
    description = models.TextField()
    tags = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="Logos", null=True, blank=True)
    favicon = models.ImageField(upload_to="Favicons", null=True, blank=True)
    theme_color = models.CharField(max_length=100, null=True, blank=True)

    cover = models.ImageField(upload_to="Covers", null=True, blank=True)
    cover_title = models.CharField(max_length=100, null=True)
    cover_description = models.TextField(max_length=150, blank=True)

    head = models.TextField(blank=True, null=True)
    script = models.TextField(blank=True, null=True)
    ads = models.CharField(
        max_length=300, verbose_name=("Ads file (ads.txt)"), null=True, blank=True
    )

    def __str__(self):
        return self.name
