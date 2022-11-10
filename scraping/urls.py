from django.urls import path
from .views import *
urlpatterns = [
    path('', index, name="home" ),
    path('p/<slug:slug>', post ),
    path('travel', blog ),
    path('search', search, name="search"),


    # Pages
    path('page/create', createPage, name='create_page'),
    path('pages', pages, name='pages'),
    path('page/<slug:slug>', page, name='page'),
    path('page/delete/<int:id>', deletePage, name='delete_page'),
    path('page/update/<int:id>', updatePage, name='update_page'),



    path('post/list/', postList, name='post-list'),



    path('contact', contact, name='contact'),
    path('lable/<str:lable>', lable, name='lable'),
    path('menu', menu, name='menu'),


    path('scraping', scraping)
]