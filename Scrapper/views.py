import bs4
from urllib.request import urlopen
from django.http import JsonResponse
import pandas as pd
import json

def FlipkartApi(request, item_name):
    response = web_scrape_flipkart(item_name).to_json(orient='records')
    return JsonResponse(json.loads(response), safe = False)

def web_scrape_flipkart(item_name):
    pages = 1
    url = 'https://www.flipkart.com/search?q=' + item_name + '&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page='
    
    page_no = 1
    Title = []
    Price = []
    Link = []
    while page_no <= pages:
        response = urlopen(url + str(page_no))
        soup = bs4.BeautifulSoup(response)
        title = soup.findAll('div', {'class': '_4rR01T'})
        prices = soup.findAll('div', {'class': '_30jeq3 _1_WHN1'})
        link = soup.findAll('a', {'class': '_1fQZEK'})
        for item in range(len(title)):
            Title.append(title[item].text)
            Price.append(prices[item].text)
            Link.append("https://www.flipkart.com" + link[item]['href'])
        page_no = page_no + 1
    data = {
    'Title': Title,
    'Price': Price,
    'Link': Link,
    }

    df = pd.DataFrame(data)
    print(df)
    return df