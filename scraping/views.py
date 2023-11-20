from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import JsonResponse
from base64 import encode
from bs4 import BeautifulSoup
import requests
from django.contrib.auth.decorators import user_passes_test
from . models import Post, Page, Contact
from django.core.paginator import Paginator
from . forms import CreateContact, FormCreatePage, PostForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext as _



def superuser_required(user):
    if not user.is_superuser:
        raise PermissionDenied
    return True

# Home page
def index(request):
    posts = Post.objects.all().order_by('-date')[0:24]
    context = {'posts': posts, 'title': "PoolsBox Travel Site"}
    return render(request, 'index.html', context)



@user_passes_test(superuser_required)
def dashobard(request):
    posts = Post.objects.filter(is_public=True).order_by('-date')
    users = User.objects.all()
    contacts = Contact.objects.filter(readed=None)
    pages = Page.objects.all()
    context = {
        'posts': posts,
        'users': users,
        'contacts': contacts,
        'pages': pages,
        'title': "Dashobard"
    }
    return render(request, 'dash.html', context)

#Travel page
def blog(request):
    content = Post.objects.all().order_by('-date')
    paginator = Paginator(content, 24) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    context = {'posts': posts, 'title': "Travel - PoolsBox Travel Site"}
    return render(request, 'blog.html', context)

# Post detail
def post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    posts = Post.objects.all().order_by('-date')[0:3]
    # Add new viewer
    post.views = post.views + 1
    post.save()

    description = post.description if post.description else False 
    


    context = {
    'title': post.title,
    'post': post,
    'posts': posts, 
    'date': post.date,
    'image': post.image.url if post.image else False,
    'tags': post.tags,
    'description': description,
    'article' : True
    }
    return render(request, 'post.html', context)



@user_passes_test(superuser_required)
def createPost(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post created successfully.')
            return redirect(request.META.get('HTTP_REFERER'))
    return render(request, 'post/update.html', {'form': form})



@user_passes_test(superuser_required)
def updatePost(request, id):
    post = get_object_or_404(Post, id=id)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            post.is_public = False
            post.save()
            messages.success(request,"Post updated successfully.")
            return redirect(f'/p/{post.slug}')
    context = {
        'post': post,
        'form': form
    }
    return render(request, 'post/update.html', context)

@user_passes_test(superuser_required)
def deletePost(request, id):
    if request.user.is_superuser :
        post = Post.objects.get(id=id)
        slug = str(post.next().slug)
        post.delete()
        messages.success(request, 'Post Deleted Succesfully..')
        return redirect(f'/p/{slug}')
    else:
        return redirect('/')


def search(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        title = Post.objects.filter(title__icontains=query)
        description = Post.objects.filter(description__icontains=query)
        posts = title | description
        context = {'posts': posts, 'title': f'Search for {query}', 'query': query}
        return render(request, 'search.html', context)
    else:
        return redirect('/')
    


#Get all users
@user_passes_test(superuser_required)
def users(request):
    content = User.objects.all().order_by('-date_joined')
    paginator = Paginator(content, 24) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    context = {'users': users, 'title': "All user"}
    return render(request, 'users/list.html', context)


@user_passes_test(superuser_required)
def contactList(request):
    content = Contact.objects.all().order_by('-date')
    paginator = Paginator(content, 24) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    contacts = paginator.get_page(page_number)
    context = {'contacts': contacts, 'title': "New contacts"}
    return render(request, 'contact/list.html', context)

@user_passes_test(superuser_required)
def contactDelete(request, id):
    contact = get_object_or_404(Contact, id=id)
    contact.delete()
    messages.success(request, "Contact deleted successfully.")
    return redirect(request.META.get('HTTP_REFERER'))

import datetime


@user_passes_test(superuser_required)
def contactRead(request, id):
    contact = get_object_or_404(Contact, id=id)
    contact.readed = datetime.datetime.now()
    contact.save()
    messages.success(request, "Contact readed successfully.")
    return redirect(request.META.get('HTTP_REFERER'))

#Travel page
@user_passes_test(superuser_required)
def postList(request):
    content = Post.objects.all().order_by('-views')
    paginator = Paginator(content, 24) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    context = {'posts': posts, 'title': "Public posts"}
    return render(request, 'post/list.html', context)

@user_passes_test(superuser_required)
def PendingPosts(request):
    content = Post.objects.filter(is_public=False).order_by('-views')
    paginator = Paginator(content, 24) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    context = {'posts': posts, 'title': "PoolsBox Travel Site"}
    return render(request, 'post/list.html', context)
# ------------------------ Page Views ----------------------

def page(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return render(request, 'page/page.html', {'page': page, "title": page.title})

@user_passes_test(superuser_required)
def pages(request):
    pages = Page.objects.all().order_by('created')
    return render(request, 'page/list.html', {'pages': pages, "title": "Pages"})


@user_passes_test(superuser_required)
def createPage(request):
    form = FormCreatePage()
    if request.method == 'POST' and request.user.is_superuser:
        form = FormCreatePage(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pages')
    context = {"form": form}
    return render(request, 'page/create.html', context)

@user_passes_test(superuser_required)
def updatePage(request, id):
    page = Page.objects.get(id=id)
    form = FormCreatePage(instance=page)
    if request.method == 'POST' and request.user.is_superuser:
        form = FormCreatePage(request.POST, instance=page)
        if form.is_valid():
            form.save()
            return redirect('pages')
    context = {"form": form}
    return render(request, 'page/update.html', context)


@user_passes_test(superuser_required)
def deletePage(request, id):
    page = Page.objects.get(id=id)
    if request.user.is_superuser:
        operation = page.delete()
        if operation:
            messages.success(request, 'Page deleted successfully.')
            return redirect('pages')

        else:
            messages.warning(request, 'Page deleted failde ')
            return redirect('pages')

    return redirect('home')


def lable(request, lable):
    posts = Post.objects.filter(title__icontains=lable)
    context = {"posts": posts, 'title': f"{lable} - PoolsBox"}
    return render(request, 'lable.html', context)

def menu(request):
    context = {'title': 'Menu - PoolsBox'}
    return render(request, 'menu.html', context)


def contact(request):
    form = CreateContact()
    if request.method == "POST":
        form = CreateContact(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'The message has been sent successfully')
            return redirect('contact')
    context = {'form':form,'title':'PoolsBox - Contace'}
    return render(request, 'contact/contact.html', context)




def postURL(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'urls.html', context)



@user_passes_test(superuser_required)
def deleteAll(request):
    posts= Post.objects.all()
    for post in posts:
        post.delete()
    return redirect('/')



































def getItem(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    soup2 = soup.find("div", class_='entry-content')
    try:
        divs = len(soup2.find_all('div'))
        scripts = len(soup2.find_all('script'))
        noscripts = len(soup2.find_all('noscript'))
        centers = len(soup2.find_all('center'))
        list = [divs, scripts, noscripts, centers]
    except:
        list = [50, 40]
    for item in range(0, max(list)):
        if soup2.find('div'):
            soup2.find('div').decompose()
        if soup.find('center'):
            soup2.find('center').decompose()
        if soup2.find('script'):
            soup2.find('script').decompose()
        if soup2.find('noscript'):
            soup2.find('noscript').decompose()
        try:
            tag = soup2.html.body
        except:
            try:
                tag = soup2.html
            except:
                tag = soup2
    return tag


def scraping(request):
    for page in range(1, 77):
        url = f"https://www.disneytouristblog.com/page/{page}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find_all("article")

        for item in results:

            title = item.find("h2").find('a').text
            try:
                image = item.find('img')['data-lazy-src']
            except:
                image = ''
            link = item.find("h2").find('a')['href']

            # Post detail scraping
            if not Post.objects.filter(title=title).exists():
                Post.objects.create(title=str(title), body=str(getItem(link)).replace('<body', '<article'))
                print("not exists...")
            print(link)
    return JsonResponse({'message': 'Scraping successfully...'})





proxy ={"http": "http://10.122.45.114:8080", "https": "http://10.122.45.114:8080"}



def getItem(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    article = soup.find("div", class_='entry-content')
    

    spans = len(article.find_all('span', class_="isc-source-text"))
    figcaption = len(article.find_all('figcaption'))
    divs = len(article.find_all('div'))

    

    
    for item in range(0, spans):
        article.find('span', class_="isc-source-text").decompose()

    for item in range(0, figcaption):
        article.find('figcaption').decompose()
    for item in range(0, divs):
        try:
            article.find('div').decompose()
        except:
            pass
    



    article = str(article).replace('<div', "<article")
    article = str(article).replace('</div', "</article")
    article = str(article).replace('www.thecrazytourist.com','www.poolsbox.com')
    return article


def scraping2(request):
    for page in range(290, 469):
        url = f"https://www.thecrazytourist.com/page/{page}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find_all("article")
        print(f"Page = {page}")
        for item in results:
            title = item.find('a').text
            try:
                image = item.find('img')['src']
            except:
                image = ''
            
            link = item.find('a')['href']
            try:
                category = item.find_all('a')[3].text
            except:
                category = ''
            try:
                tags = item.find_all('a')[4].text
            except:
                tags = ''
            description = item.find('p').text[0:159]
            # Post detail scraping
            if not Post.objects.filter(title=title).exists():
                Post.objects.create(title=str(title), category=str(category), tags=str(tags), description=str(description), body=str(getItem(link)))
                print("Not exists...")
            print(link)

    return JsonResponse({'message': 'Scraping successfully...'})