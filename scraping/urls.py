from django.urls import path
from . views import *
from .sites.theplanetd import theplanetd
from .sites.tourscanner import tourscanner



urlpatterns = [
    path('', index, name="home" ),
    path('dashboard', dashobard, name="dashobard"),
    path('p/<slug:slug>', post ),
    path('p/<slug:slug>/', post ),
    path('travel', blog ),
    path('search', search, name="search"),


    # Pages
    path('page/create', createPage, name='create_page'),
    path('pages', pages, name='pages'),
    path('page/<slug:slug>', page, name='page'),
    path('page/delete/<int:id>', deletePage, name='delete_page'),
    path('page/update/<int:id>', updatePage, name='update_page'),

    path('users', users, name="users"),
    path('contact/list', contactList),
    path('contact/delete/<int:id>', contactDelete),
    path('contact/read/<int:id>', contactRead),



    path('post/list/', postList, name='post-list'),
    path('post/create', createPost, name="create_post"),
    path('post/update/<int:id>', updatePost, name="update_post"),
    path('post/delete/<int:id>', deletePost, name='delete_post'),



    path('contact', contact, name='contact'),
    path('lable/<str:lable>', lable, name='lable'),
    path('menu', menu, name='menu'),
    path('urls', postURL),


    path('delete-all', deleteAll),


    path('scraping', scraping),
    path('scraping2', scraping2),
    path('theplanetd', theplanetd),
    path('tourscanner', tourscanner)
]