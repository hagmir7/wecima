from django.db import models
from django.contrib.auth.models import User





class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=150)
    category = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='Image',null=True, blank=True)
    image_link = models.CharField(max_length=2000,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    views = models.IntegerField(default=0)
    tages = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    slug = models.SlugField(null=True, blank=True)



    def __str__(self):
        return self.title