from django.http.response import JsonResponse
from base64 import encode
from bs4 import BeautifulSoup
import requests
from scraping.models import Post

#  https://tourscanner.com/blog/
proxy ={"http": "http://10.122.114.61:8080", "https": "http://10.122.114.61:8080"}

# Remove end spaces
def remove_end_spaces(string):
    return "".join(string.rstrip())

# Remove first and  end spaces
def remove_first_end_spaces(string):
    return "".join(string.rstrip().lstrip())

# Remove all spaces
def remove_all_spaces(string):
    return "".join(string.split())

# Remove all extra spaces
def remove_all_extra_spaces(string):
    return " ".join(string.split())




def getItem(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    article = soup.find("div", class_='td-post-content')
    if article == None:
        return None
    # return article
    try:
        article.find('div', class_="at-above-post").decompose()
    except:
        pass
    
    # for item in range(0, spans):
    #     article.find('span', class_="isc-source-text").decompose()

    try:
        for item in range(0, len(article.find_all('figcaption'))):
            article.find('figcaption').decompose()
    except:
        pass
    
    for item in range(0, len(article.find_all('script'))):
        try:
            article.find('script').decompose()
        except:
            pass


    for item in range(0, len(article.find_all('ul'))):
        try:
            article.find('ul').decompose()
        except:
            pass
    for item in range(0, len(article.find_all('ins'))):
        try:
            article.find('ins').decompose()
        except:
            pass

        
    # article = str(article).replace('https://tourscanner.com/blog/', 'www.poolsbox.com/p/')
    return article




def getTags(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    tags = soup.find_all("li", class_='entry-category')
    new_tags = []
    for tag in tags:
        new_tags.append(str(tag.text))

    return ",".join(new_tags)


def tourscanner(request):
    for page in range(46 , 0 , -1):
        print(f"Page == {page}")
        url = f"https://tourscanner.com/blog/page/{page}/"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all("div", class_="td_module_18")
        # print(results)
        for item in results:
            print("Ready...")
            if item:
                title = item.find_all('a')[1].text
                image = item.find('img', class_="entry-thumb")['src']
                link = item.find_all('a')[1]['href']
                description = str(item.find('div', class_="td-excerpt")).replace('<div class="td-excerpt">', '')
                description = description.replace('</div>', '')
                description = remove_first_end_spaces(description)
                # tags = item.find('span', class_="tagContent")

                if not Post.objects.filter(title=title).exists():
                    Post.objects.create(title=str(title), tags=str(getTags()), description=str(description), image_link=str(image), body=str(getItem(link)))
                    print("not exists...")
                else:
                    post = Post.objects.get(title=str(title))
                    if 'function' in str(post.tags):
                       post.tags = str(getTags(link))
                       post.save()
                       print('Updated successfully...')
                print(link)
    return JsonResponse({"message": "Successfully..."})