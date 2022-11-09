from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.crypto import get_random_string





class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.TextField(max_length=150)
    category = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='Image',null=True, blank=True)
    image_link = models.TextField(max_length=2000,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    views = models.IntegerField(default=0)
    tags = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    slug = models.SlugField(null=True, blank=True)
    is_public = models.BooleanField(default=True)



    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.id:
            self.slug = self.slug
        else:
            self.slug = slugify(self.title)

        super(Post, self).save(*args, **kwargs)




class Page(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        random = get_random_string(length=5)
        if self.id:
            self.slug = self.slug
        else:
            self.slug = slugify(self.title +"-"+ str(random))

        super(Page, self).save(*args, **kwargs)


# Contact
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name