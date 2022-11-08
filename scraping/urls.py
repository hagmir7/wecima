from django.urls import path
from .views import index, scraping
urlpatterns = [
    path('', index, name="home" ),
    path('scraping', scraping)   
]