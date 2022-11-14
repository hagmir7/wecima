# from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import JsonResponse
from base64 import encode
from bs4 import BeautifulSoup
import requests
from scraping.models import Post




proxy ={"http": "http://10.122.90.200:8080", "https": "http://10.122.90.200:8080"}


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


    for item in range(0, len(article.find_all('ul'))):
        try:
            article.find('ul').decompose()
        except:
            pass







    article = str(article).replace('<div', "<article")
    article = str(article).replace('</div', "</article")
    article = str(article).replace('theplanetd.com', 'www.poolsbox.com/p')
    return article


def theplanetd(request):
    for page in range(1, 177):
        url = f"https://theplanetd.com/travel-blog/page/{page}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find_all("article")
        print(f"Page == {page}")
        for item in results:
            title = item.find_all('a')[1].text
            image = item.find('img')['data-pin-media']
            link = item.find('a')['href']
            category = item.find_all('a')[-1].text
            tags = item.find_all('a')[-1].text
            description = item.find('p').text[0:159]
            if not Post.objects.filter(title=title).exists():
                Post.objects.create(title=str(title), category=str(category), tags=str(tags), description=str(description), image_link=str(image), body=str(getItem(link)))
                print("not exists...")
            print(link)
    return JsonResponse({"message": "Successfully..."})