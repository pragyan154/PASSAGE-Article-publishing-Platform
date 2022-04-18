import requests
from bs4 import BeautifulSoup 


Url = "https://indianexpress.com/latest-news/"

page = requests.get(Url)

soup = BeautifulSoup(page.text , "html.parser")

def news_scrapper():
    news_list = []
    headings = soup.find_all('div', {"class": "title"})
    # print(headings[0].contents)
    for h in headings:
        news_title = h.text
        el = h.find('a', href=True)
        e = (el['href'])
        news_list.append({"link":e ,"title":news_title})
    return news_list

