from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import JsonResponse
from bs4 import BeautifulSoup
import requests
from .models import *
from django.core.paginator import Paginator
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.views import View
from django.http import Http404

try:
    settings = Settings.objects.last()
except:
    settings = False


def superuser_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404("The requested resource does not exist.")
        if not request.user.is_authenticated:
            return redirect("login")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


class AdsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "ads.txt")


# Home page
def index(request):
    posts = Post.objects.all().order_by("-date")[0:24]
    title = getattr(settings, "title", "Blog Website Create by Freesad.com")
    context = {"posts": posts, "title": title}
    return render(request, "index.html", context)


@superuser_required
def dashobard(request):
    posts = Post.objects.filter(is_public=True).order_by("-date")
    users = User.objects.all()
    contacts = Contact.objects.filter(readed=None)
    pages = Page.objects.all()
    context = {
        "posts": posts,
        "users": users,
        "contacts": contacts,
        "pages": pages,
        "title": "لوحة التحكم",
    }
    return render(request, "dash.html", context)


# Travel page
def blog(request):
    content = Post.objects.all().order_by("-date")
    paginator = Paginator(content, 24)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)
    title = getattr(settings, "title", "No title yet")
    context = {"posts": posts, "title": f"مواضيع - {title}"}
    return render(request, "blog.html", context)


# Post detail
def post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    posts = Post.objects.all().order_by("-date")[0:3]

    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    if not IpModel.objects.filter(ip=ip).exists():
        location = IpModel.objects.create(ip=ip)
    else:
        location = IpModel.objects.get(ip=ip)

    if not location in post.views.all():
        post.views.add(location)
        post.save()

    description = post.description if post.description else False

    context = {
        "title": post.title,
        "post": post,
        "posts": posts,
        "date": post.date,
        "image": post.image.url if post.image else False,
        "tags": post.tags,
        "description": description,
        "article": True,
    }
    return render(request, "post.html", context)


@superuser_required
def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "تم إنشاء الصنف بنجاح")
            return redirect(request.META.get("HTTP_REFERER"))
    else:
        form = CategoryForm()

    return render(request, "category/create.html", {"form": form})


@superuser_required
def update_category(request, slug):
    category = get_object_or_404(Category, slug=slug)

    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تعديل الصنف بنجاح.")
            return redirect(request.META.get("HTTP_REFERER"))
    else:
        form = CategoryForm(instance=category)

    return render(request, "category/create.html", {"form": form, "category": category})


@superuser_required
def delete_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    delete = category.delete()
    if delete:
        messages.success(request, "تم حذف المقال بنجاح.")
        return redirect("category_list")
    else:
        messages.warning(request, "Fail to delete category", extra_tags="danger")
        return redirect(request.META.get("HTTP_REFERER"))


@superuser_required
def list_category(request):
    content = Category.objects.all()
    paginator = Paginator(content, 40)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    categories = paginator.get_page(page_number)
    context = {"categories": categories}
    return render(request, "category/list.html", context)


@superuser_required
def createPost(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "تم إنشاء المقال بنجاح")
            return redirect(request.META.get("HTTP_REFERER"))
    return render(
        request, "post/update.html", {"form": form, "title": "إنشاء أو حذف المقال"}
    )


@superuser_required
def updatePost(request, id):
    post = get_object_or_404(Post, id=id)
    form = PostForm(instance=post)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post, files=request.FILES)
        if form.is_valid():
            form.save()
            post.is_public = False
            post.save()
            messages.success(request, "تم تعديل المقال بنجاح.")
            return redirect(f"/p/{post.slug}")
    context = {"post": post, "form": form}
    return render(request, "post/update.html", context)


@superuser_required
def deletePost(request, id):
    if request.user.is_superuser:
        post = Post.objects.get(id=id)
        try:
            slug = str(post.next().slug)
        except:
            pass
        post.delete()
        messages.success(request, "تم حذف المقال بنجاح.")
        if request.GET.get("post"):
            try:
                return redirect(f"/p/{slug}")
            except:
                return redirect("/post/list/")
        else:
            return redirect("/post/list/")
    else:
        return redirect("/")


def search(request):
    if request.method == "GET":
        query = request.GET.get("query")
        title = Post.objects.filter(title__icontains=query)
        description = Post.objects.filter(description__icontains=query)
        posts = title | description
        context = {"posts": posts, "title": f"بحث عن {query}", "query": query}
        return render(request, "search.html", context)
    else:
        return redirect("/")


# Get all users
@superuser_required
def users(request):
    content = User.objects.all().order_by("-date_joined")
    paginator = Paginator(content, 24)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    users = paginator.get_page(page_number)
    context = {"users": users, "title": "كل المتخدمين"}
    return render(request, "users/list.html", context)


@superuser_required
def contactList(request):
    content = Contact.objects.all().order_by("-date")
    paginator = Paginator(content, 24)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    contacts = paginator.get_page(page_number)
    context = {"contacts": contacts, "title": "راسائل جديدة"}
    return render(request, "contact/list.html", context)


@superuser_required
def contactDelete(request, id):
    contact = get_object_or_404(Contact, id=id)
    contact.delete()
    messages.success(request, "تم حدف الرسالة بنجاح.")
    return redirect(request.META.get("HTTP_REFERER"))


import datetime


@superuser_required
def contactRead(request, id):
    contact = get_object_or_404(Contact, id=id)
    contact.readed = datetime.datetime.now()
    contact.save()
    messages.success(request, "Contact readed successfully.")
    return redirect(request.META.get("HTTP_REFERER"))


# Travel page
@superuser_required
def postList(request):
    content = Post.objects.all().order_by("-views")
    paginator = Paginator(content, 24)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)
    context = {"posts": posts, "title": "مقالات عامة"}
    return render(request, "post/list.html", context)


@superuser_required
def PendingPosts(request):
    content = Post.objects.filter(is_public=False).order_by("-views")
    paginator = Paginator(content, 24)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)
    context = {"posts": posts, "title": "Pending Posts"}
    return render(request, "post/list.html", context)


# ------------------------ Page Views ----------------------


def page(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return render(request, "page/page.html", {"page": page, "title": page.title})


@superuser_required
def pages(request):
    pages = Page.objects.all().order_by("created")
    return render(request, "page/list.html", {"pages": pages, "title": "الصفحات"})


@superuser_required
def createPage(request):
    form = FormCreatePage()
    if request.method == "POST" and request.user.is_superuser:
        form = FormCreatePage(request.POST)
        if form.is_valid():
            form.save()
            return redirect("pages")
    context = {"form": form}
    return render(request, "page/create.html", context)


@superuser_required
def updatePage(request, id):
    page = Page.objects.get(id=id)
    form = FormCreatePage(instance=page)
    if request.method == "POST" and request.user.is_superuser:
        form = FormCreatePage(request.POST, instance=page)
        if form.is_valid():
            form.save()
            return redirect("pages")
    context = {"form": form}
    return render(request, "page/update.html", context)


@superuser_required
def links(request):
    content = Link.objects.all().order_by("-created_at")
    paginator = Paginator(content, 24)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    links = paginator.get_page(page_number)

    context = {"links": links, "title": "تعديل الروابط"}
    return render(request, "configuration/links/list.html", context)


@superuser_required
def create_link(request):
    if request.method == "POST":
        form = LinkForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تم إنشاء الرابط بنجاح")
            return redirect(request.META.get("HTTP_REFERER"))
    messages.warning(request, "Fail to created link.")
    return redirect(request.META.get("HTTP_REFERER"))


@superuser_required
def link_delete(request, id):
    link = get_object_or_404(Link, id=id)
    if link:
        link.delete()
        messages.success(request, "تم حدف الرابط")
        return redirect(request.META.get("HTTP_REFERER"))
    messages.warning(request, "فشل حذف الروابط.", extra_tags="danger")
    return redirect(request.META.get("HTTP_REFERER"))


@superuser_required
def link_update(request, id):
    link = get_object_or_404(Link, id=id)
    form = LinkForm(instance=link)

    if request.method == "POST":
        form = LinkForm(request.POST, instance=link)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تعديل الربط.")
            return redirect(request.META.get("HTTP_REFERER"))

    return render(request, "configuration/links/update.html", {"form": form})


@superuser_required
def site_info(request):
    settings = Settings.objects.last()

    if request.method == "POST":
        if settings:
            form = SiteInfoForm(request.POST, request.FILES, instance=settings)
        else:
            form = SiteInfoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Site info is updated successfully.")
            return redirect(request.META.get("HTTP_REFERER"))

    else:  # For GET requests
        form = SiteInfoForm(instance=settings) if settings else SiteInfoForm()

    return render(request, "configuration/site/info.html", {"form": form})


@superuser_required
def cover(request):
    settings = Settings.objects.last()
    if request.method == "POST":
        if settings:
            form = CoverForm(request.POST, request.FILES, instance=settings)
        else:
            form = CoverForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "Cover is updated successfully.")
            return redirect(request.META.get("HTTP_REFERER"))

    else:  # For GET requests
        form = CoverForm(instance=settings) if settings else CoverForm()
    return render(request, "configuration/site/cover.html", {"form": form})


@superuser_required
def advanced(request):
    settings = Settings.objects.last()
    if request.method == "POST":
        if settings:
            form = AdvancedForm(request.POST, request.FILES, instance=settings)
        else:
            form = AdvancedForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "Cover is updated successfully.")
            return redirect(request.META.get("HTTP_REFERER"))

    else:  # For GET requests
        form = AdvancedForm(instance=settings) if settings else AdvancedForm()
    return render(request, "configuration/site/advanced.html", {"form": form})


@superuser_required
def deletePage(request, id):
    page = Page.objects.get(id=id)
    if request.user.is_superuser:
        operation = page.delete()
        if operation:
            messages.success(request, "Page deleted successfully.")
            return redirect("pages")

        else:
            messages.warning(request, "Page deleted failde ")
            return redirect("pages")

    return redirect("home")


def lable(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.post_category.all()

    # Access the project's name from settings
    title = getattr(settings, "title", "No title yet")

    context = {"posts": posts, "title": f"{category.name}"}
    return render(request, "lable.html", context)


def menu(request):
    title = getattr(settings, "title", "No title yet")

    context = {"title": f"القائمة - {title}"}
    return render(request, "menu.html", context)


def contact(request):
    form = CreateContact()
    if request.method == "POST":
        form = CreateContact(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تم إرسال الرسالة")
            return redirect("contact")

    title = getattr(settings, "title", "No title yet")
    context = {"form": form, "title": f"تواصل معنا - {title}"}
    return render(request, "contact/contact.html", context)


def postURL(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "urls.html", context)


@superuser_required
def deleteAll(request):
    posts = Post.objects.all()
    for post in posts:
        post.delete()
    return redirect("/")


def getItem(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    soup2 = soup.find("div", class_="entry-content")
    try:
        divs = len(soup2.find_all("div"))
        scripts = len(soup2.find_all("script"))
        noscripts = len(soup2.find_all("noscript"))
        centers = len(soup2.find_all("center"))
        list = [divs, scripts, noscripts, centers]
    except:
        list = [50, 40]
    for item in range(0, max(list)):
        if soup2.find("div"):
            soup2.find("div").decompose()
        if soup.find("center"):
            soup2.find("center").decompose()
        if soup2.find("script"):
            soup2.find("script").decompose()
        if soup2.find("noscript"):
            soup2.find("noscript").decompose()
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
            title = item.find("h2").find("a").text
            try:
                image = item.find("img")["data-lazy-src"]
            except:
                image = ""
            link = item.find("h2").find("a")["href"]

            # Post detail scraping
            if not Post.objects.filter(title=title).exists():
                Post.objects.create(
                    title=str(title),
                    body=str(getItem(link)).replace("<body", "<article"),
                )
                print("not exists...")
            print(link)
    return JsonResponse({"message": "Scraping successfully..."})


proxy = {"http": "http://10.122.45.114:8080", "https": "http://10.122.45.114:8080"}


def getItem(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    article = soup.find("div", class_="entry-content")

    spans = len(article.find_all("span", class_="isc-source-text"))
    figcaption = len(article.find_all("figcaption"))
    divs = len(article.find_all("div"))

    for item in range(0, spans):
        article.find("span", class_="isc-source-text").decompose()

    for item in range(0, figcaption):
        article.find("figcaption").decompose()
    for item in range(0, divs):
        try:
            article.find("div").decompose()
        except:
            pass

    article = str(article).replace("<div", "<article")
    article = str(article).replace("</div", "</article")
    article = str(article).replace("www.thecrazytourist.com", "www.merylivre.com")
    return article


def scraping2(request):
    for page in range(290, 469):
        url = f"https://www.thecrazytourist.com/page/{page}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find_all("article")
        print(f"Page = {page}")
        for item in results:
            title = item.find("a").text
            try:
                image = item.find("img")["src"]
            except:
                image = ""

            link = item.find("a")["href"]
            try:
                category = item.find_all("a")[3].text
            except:
                category = ""
            try:
                tags = item.find_all("a")[4].text
            except:
                tags = ""
            description = item.find("p").text[0:159]
            # Post detail scraping
            if not Post.objects.filter(title=title).exists():
                Post.objects.create(
                    title=str(title),
                    category=str(category),
                    tags=str(tags),
                    description=str(description),
                    body=str(getItem(link)),
                )
                print("Not exists...")
            print(link)

    return JsonResponse({"message": "Scraping successfully..."})
