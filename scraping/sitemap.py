from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post


class StaticViewSitemap(Sitemap):

    def items(self):
        return ['home']
    
    def location(self, items):
        return reverse(items)


class PostsSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5
    def items(self):
        return Post.objects.all()