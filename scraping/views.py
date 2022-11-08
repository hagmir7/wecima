from django.shortcuts import render
from django.http.response import JsonResponse
from base64 import encode
from bs4 import BeautifulSoup
import requests
from .models import Post


def index(request):
    return render(request, 'index.html')


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
        url = f"https://www.nomadicmatt.com/travel-blog/page/{page}/"
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
                Post.objects.create(title=str(title), image_link=str(image), body=str(getItem(link)).replace('<body', '<article'))
                print("not exists...")
            print(link)
    return JsonResponse({'message': 'Scraping successfully...'})
